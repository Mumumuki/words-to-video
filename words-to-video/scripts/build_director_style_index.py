"""Build a searchable Markdown index from the user-provided director style PDF.

Usage: python build_director_style_index.py input.pdf output.md
Requires: pypdf
"""

import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader


def clean(line):
    normalized = unicodedata.normalize("NFKC", line.replace("\x01", " "))
    return re.sub(r"\s+", " ", normalized).strip()


def cell(text):
    return clean(text).replace("|", "／")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python build_director_style_index.py input.pdf output.md")

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    reader = PdfReader(str(source))
    entries = {}
    current = None
    category = "未分类"

    for page_number, page in enumerate(reader.pages, start=1):
        if page_number < 4:
            continue
        for raw_line in (page.extract_text() or "").splitlines():
            line = clean(raw_line)
            if not line:
                continue
            category_match = re.match(r"^(\d{2})\s+(.+)$", line)
            director_match = re.match(r"^(\d{3})\s+(.+)$", line)
            if director_match:
                director_id, name = director_match.groups()
                if director_id not in entries:
                    current = {
                        "id": director_id,
                        "name": clean(name),
                        "category": category,
                        "page": page_number,
                        "parts": [],
                    }
                    entries[director_id] = current
                else:
                    current = entries[director_id]
                continue
            if category_match:
                category = clean(category_match.group(2))
                current = None
                continue
            if current is not None and not line.startswith("全 200 位速查"):
                current["parts"].append(line)

    expected = {f"{number:03d}" for number in range(1, 201)}
    missing = sorted(expected - set(entries))
    extra = sorted(set(entries) - expected)
    if missing or extra:
        raise RuntimeError(f"Director ID mismatch; missing={missing}, extra={extra}")

    lines = [
        "# 导演视觉风格灵感索引",
        "",
        f"> 来源：用户提供的导演风格图册 PDF（共 {len(reader.pages)} 页，**未随技能包分发**，只留本索引）。{len(entries)} 条摘要已按页提取完毕，日常使用只查本索引即可，不再需要原书；如需重新生成或换一本图册，用 `scripts/build_director_style_index.py`（依赖 pypdf）重跑，页码列对应原书页序。",
        "> 只作风格灵感与检索提示，不作项目风格锚点，不把PDF页面视为用户提供的参考图，不替代第五步六维风格卡协商。",
        "> 仅在用户没有明确风格或主动要求建议时使用。默认推荐1个主要方向和1个备选，并说明与来源材料、时长和内容类型（`剧情演绎`／`MV`）的适配理由；禁止一次输出完整200位清单。",
        "> 摘要按PDF原文提取，未独立核验其导演风格判断；不得据此伪造历史、形制或作品考据。",
        "> **题材筛选规则**：索引内导演风格以古典/古装向居多。古典项目优先取古典向；现代项目按都市写实、生活流筛选；科幻项目按硬科幻工业、近未来日常筛选。**不把导演名直接当风格锚点**，也不把某一导演的整部作品风格照搬为本项目定稿——最终仍以第五步六维风格卡为准。",
        "",
        "| 编号 | 导演 | 分类 | 原书页码 | 风格摘要与视觉线索 |",
        "|---|---|---|---|---|",
    ]
    for director_id in sorted(entries):
        entry = entries[director_id]
        summary = " ".join(entry["parts"])
        lines.append(
            f"| {entry['id']} | {cell(entry['name'])} | {cell(entry['category'])} | {entry['page']} | {cell(summary)} |"
        )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    incomplete = [entry["id"] for entry in entries.values() if not entry["parts"]]
    print(f"Indexed {len(entries)} directors from {len(reader.pages)} pages; incomplete={incomplete}")


if __name__ == "__main__":
    main()
