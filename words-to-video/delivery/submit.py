#!/usr/bin/env python3
"""words-to-video 可迁移交付提交器。

把 S14 产出的填表包（package/）在 S15 步骤按段提交到 AI 视频生成平台。
铁律（继承 SKILL 第 18 / 479 行）：未获显式同意（--consent）只产出执行计划（--dry-run 默认）。

用法：
  python delivery/submit.py --package package/ --config delivery/config.example.json \
      --adapter comfyui_local --consent [--segments P01 P02] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# 让脚本在 delivery/ 下可直接 import adapters
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import load_adapter  # noqa: E402


def find_segments(package_dir: Path) -> list[str]:
    return sorted(
        p.name for p in package_dir.iterdir()
        if p.is_dir() and p.name.startswith("P")
    )


def build_payload(seg_dir: Path) -> dict:
    prompt_file = seg_dir / "prompt.txt"
    prompt = prompt_file.read_text(encoding="utf-8") if prompt_file.exists() else ""
    refs_dir = seg_dir / "refs"
    refs = sorted(str(p) for p in refs_dir.glob("*.png")) if refs_dir.exists() else []
    handoff_dir = seg_dir / "handoff"
    first = str(next(handoff_dir.glob("*first*"), "")) if handoff_dir.exists() else ""
    last = str(next(handoff_dir.glob("*last*"), "")) if handoff_dir.exists() else ""
    sheet = seg_dir / "sheet.md"
    return {
        "segment_id": seg_dir.name,
        "prompt": prompt,
        "refs": refs,
        "handoff_first": first,
        "handoff_last": last,
        "sheet": sheet.read_text(encoding="utf-8") if sheet.exists() else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="words-to-video 交付提交器（配置驱动）")
    ap.add_argument("--package", required=True, help="S14 产出的填表包目录（由 S15 调用）")
    ap.add_argument("--config", default=None, help="配置文件 json")
    ap.add_argument("--adapter", default=None, help="适配器名（覆盖 config 的 default_adapter）")
    ap.add_argument("--segments", nargs="*", default=None, help="只提交指定段落，如 P01 P02")
    ap.add_argument("--consent", action="store_true", help="已获用户显式同意（硬性闸门）")
    ap.add_argument("--dry-run", action="store_true", help="只出执行计划，不调用接口")
    args = ap.parse_args()

    pkg = Path(args.package)
    if not pkg.is_dir():
        print(f"[错误] 填表包目录不存在：{pkg}", file=sys.stderr)
        return 2

    cfg_path = Path(args.config) if args.config else Path(__file__).resolve().parent / "config.example.json"
    config = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    adapter_name = args.adapter or config.get("default_adapter")
    if not adapter_name:
        print("[错误] 未指定 adapter", file=sys.stderr)
        return 2
    adapter_cfg = config.get("adapters", {}).get(adapter_name)
    if not adapter_cfg:
        print(f"[错误] 配置中找不到适配器：{adapter_name}", file=sys.stderr)
        return 2

    segments = find_segments(pkg)
    if args.segments:
        segments = [s for s in segments if s in args.segments]
    if not segments:
        print("[错误] 未找到任何 P 段", file=sys.stderr)
        return 2

    # 显式同意闸门（继承 SKILL 第 18 / 479 行）
    consent_required = config.get("consent_required", True)
    really_submit = args.consent and not args.dry_run
    if consent_required and not really_submit:
        print("[计划] 未获显式同意或 --dry-run，仅输出执行计划，不提交：")
        for s in segments:
            p = build_payload(pkg / s)
            print(f"  - {s}: prompt={len(p['prompt'])}字, refs={len(p['refs'])}张, "
                  f"handoff={bool(p['handoff_first'])}/{bool(p['handoff_last'])}")
        return 0

    # 真实提交
    adapter = load_adapter(adapter_cfg)
    manifest = {"adapter": adapter_name, "segments": []}
    print(f"[提交] 适配器={adapter_name}, 段落={segments}")
    for s in segments:
        p = build_payload(pkg / s)
        try:
            job_id = adapter.submit(p)
            status, detail = "running", ""
            deadline = time.time() + adapter_cfg.get("timeout_sec", 600)
            while status == "running" and time.time() < deadline:
                time.sleep(adapter_cfg.get("poll_interval_sec", 3))
                status, detail = adapter.get_status(job_id)
            manifest["segments"].append({"segment": s, "job_id": job_id, "status": status, "detail": detail})
            print(f"  - {s}: job={job_id} status={status} {detail}")
        except Exception as e:  # 单段失败不阻塞其余段
            manifest["segments"].append({"segment": s, "job_id": None, "status": "failed", "detail": str(e)})
            print(f"  - {s}: 提交异常 {e}", file=sys.stderr)

    out = pkg.parent / "delivery-manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[完成] manifest -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
