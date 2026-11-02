#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_storyboard.py —— 第十二步 c 段「A 类几何项」校验脚本。

用途：把故事板的排版几何从「目测」变成「出数」。按 --layout 适配两版式：

  table  展示版·六区段落板（给人看）：2400×2960。
         检查：A1 N 格互不雷同、A2 每格画面区 16:9、A3 ④ 区按 grid_of(N) 对齐且未压边、
               A4 画幅、A5 cells 源图、A6 题头深色带、A7 ④ 两行画面带的高度与位置。
         做法不是「盲测结构」，而是按已知几何复算、再到预期位置采样核对。

  raw    模型版（给视频模型）：2×3 网格、零文字、每格严格 16:9。
         检查：A1 N 格互不雷同、A2 每格 16:9、A3 grid_of(N) 网格放得下且比例正确、A4 整张宽 2352 高随格数扩展、
               A5 cells 源图、A6 **顶部无页眉带/无文字**。
         这一版没有六区分带，**不评 A7**。
         这一版专供裁切成单帧喂图生视频，所以「零文字」与「每格 16:9」是硬指标。

输出顺序固定 A1→A7（与 `storyboard-selfcheck.md` 的表一致）。

用法：
  python scripts/verify_storyboard.py --image SB-01-table.png --layout table --cells cells --prefix P01
  python scripts/verify_storyboard.py --image SB-01-raw.png --layout raw --cells cells --prefix P01

依赖：Pillow（pip install pillow）。Windows 下若默认 python 无 PIL，可用带 Pillow 的解释器。
"""

import argparse
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    print("需要 Pillow：pip install pillow")
    sys.exit(2)

TARGET_RATIO = 16.0 / 9.0
RATIO_TOL = 0.01

# ---- 展示版六区几何（4k，f=1.0；与 build_storyboard.py 同源）----
T_W, T_H = 2400, 2960
T_PAD = 72
T_HEADER = 200
T_BAND_Y, T_BAND_H = 244, 720
T_CELL_W, T_CELL_H, T_IMG_H, T_ROW_GAP = 725, 620, 408, 40
T_BOARD_Y = 1104

# raw 版基准（4k，f=1.0）
RAW_W, RAW_H, RAW_GAP = 2352, 1000, 10

LAYOUTS = {
    "table": dict(grid=False, header=True),
    "raw": dict(grid=True, header=False),
}


def ratio(w, h):
    return w / float(h) if h else 0.0


# 结果先记录、最后按 A1→A7 顺序统一打印：各项的检查顺序受实现影响（画幅要先于
# 格内比例算），但给人看的表必须按编号排，否则文档写的顺序与实际输出对不上。
ORDER = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
_ROWS = []


def line(no, name, detail, ok):
    _ROWS.append((no, name, detail, ok))
    return ok


def flush_rows():
    def width(s):
        return sum(2 if ord(ch) > 127 else 1 for ch in s)

    def pad_to(s, n):
        return s + " " * max(0, n - width(s))

    idx = dict((k, i) for i, k in enumerate(ORDER))
    for no, name, detail, ok in sorted(_ROWS, key=lambda r: idx.get(r[0], 99)):
        print("  %s %s %s %s" % (pad_to(no, 3), pad_to(name, 20),
                                 pad_to(detail, 58), "PASS" if ok else "FAIL"))


def raw_grid_geometry(W, cols=3):
    """复算 build_raw 的格几何，返回 (gw, gh, gap)。

    格宽必须按列数分：格数少时列数变少、格变大。固定按 3 列复算会在 2 列
    （4 格 2×2）时算出偏小的格，A2/A3/A6 的采样位置会整体错位——A6 会因此
    把「网格上方的留白」算到画面里，误报成有页眉。
    """
    f = W / float(RAW_W)
    gap = max(1, int(RAW_GAP * f))
    gw = ((W - gap * (cols + 1)) // cols) // 16 * 16
    gh = gw * 9 // 16
    return gw, gh, gap


INFO_H = 212          # 格内信息区高度（620 − 408），格数变化时保持不变
T_STEP = 40           # 格间距


def grid_of(n):
    """格数 → (列, 行)，与 build_storyboard.grid_of 同源。2–3 格单行、4 格 2×2、5–6 格 3×2。"""
    if n <= 3:
        return n, 1
    if n == 4:
        return 2, 2
    return 3, 2


def table_geometry(expect, f=1.0):
    """按格数复算 ④ 区几何：(cols, rows, cell_w, img_h, cell_h, step, pad)。"""
    W = int(T_W * f)
    pad = int(T_PAD * f)
    rw = W - pad * 2
    step = int(T_STEP * f)
    cols, rows = grid_of(expect)
    if cols == 3:
        return cols, rows, int(T_CELL_W * f), int(T_IMG_H * f), int(T_CELL_H * f), step, pad
    cw = (rw - step * (cols - 1)) // cols
    ih = cw * 9 // 16
    return cols, rows, cw, ih, ih + int(INFO_H * f), step, pad


def table_height(expect, f=1.0):
    """按格数复算整张高度（4k 基准常量 × f）。"""
    _c, rows, _cw, _ih, ch, _s, _p = table_geometry(expect, f)
    board_h = ch * rows + int(T_ROW_GAP * f) * (rows - 1)
    return (int(T_HEADER * f) + int(44 * f) + int(T_BAND_H * f) + int(40 * f)
            + int(100 * f) + board_h + int(56 * f) + int(400 * f)
            + int(60 * f) + int(60 * f))


def band_stats(img, y0, y1):
    """取一条横带的灰度均值与标准差，判断是否为均匀纯色带。"""
    crop = img.crop((0, y0, img.size[0], y1)).convert("L").resize((64, 8))
    px = list(crop.tobytes())
    mean = sum(px) / float(len(px))
    var = sum((p - mean) ** 2 for p in px) / float(len(px))
    return mean, var ** 0.5


def patch_rgb(img, cx, cy, r=8):
    """取一小块的平均色，用于判断「这里是画面还是底色」。"""
    W, H = img.size
    box = (max(0, cx - r), max(0, cy - r), min(W, cx + r), min(H, cy + r))
    if box[2] <= box[0] or box[3] <= box[1]:
        return (128, 128, 128)
    c = img.crop(box).convert("RGB")
    px = c.tobytes()
    n = max(1, len(px) // 3)
    return (sum(px[0::3]) / n, sum(px[1::3]) / n, sum(px[2::3]) / n)


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def row_profile(img, sample_w=64):
    """每行的灰度标准差剖面，用于定位分镜画面带（照片带方差大）。"""
    small = img.convert("L").resize((sample_w, img.size[1]))
    W_s, H_s = small.size
    px = small.tobytes()
    prof = []
    for y in range(H_s):
        band = px[y * W_s:(y + 1) * W_s]
        m = sum(band) / float(W_s)
        var = sum((p - m) ** 2 for p in band) / float(W_s)
        prof.append(var ** 0.5)
    return prof


def bands(prof, thresh, min_h, y0, y1, tol_gap=12):
    """在 y0..y1 内找高方差连续带，返回 [(start, end), ...]。"""
    out, cur = [], None
    for y in range(max(0, y0), min(len(prof), y1)):
        hot = prof[y] > thresh
        if hot and cur is None:
            cur = y
        elif not hot and cur is not None:
            if y - cur >= min_h:
                out.append((cur, y))
            cur = None
    if cur is not None and min(len(prof), y1) - cur >= min_h:
        out.append((cur, min(len(prof), y1)))
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= tol_gap:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def main():
    ap = argparse.ArgumentParser(description="故事板几何校验（第十二步 c 段 A 类，两版式）")
    ap.add_argument("--image", required=True, help="整张故事板图片路径")
    ap.add_argument("--cells", default="", help="单格裁切文件目录（用于 A5）")
    ap.add_argument("--layout", choices=["table", "raw"], default="table",
                    help="版式：table 六区段落板 / raw 模型版")
    ap.add_argument("--expect", type=int, default=6, help="期望格数，默认 6")
    ap.add_argument("--crop-to", default="", help="可选：按几何从 raw 版裁出单格并写入该目录")
    ap.add_argument("--prefix", default="", help="源图文件名前缀，如 P01")
    args = ap.parse_args()

    path = os.path.abspath(args.image)
    if not os.path.exists(path):
        print("找不到图片：%s" % path)
        return 2

    img = Image.open(path).convert("RGB")
    W, H = img.size
    spec = LAYOUTS[args.layout]
    f = W / float(T_W if args.layout == "table" else RAW_W)
    print("\n[Storyboard Verify] %s  (layout=%s, %dx%d, f=%.2f)"
          % (os.path.basename(path), args.layout, W, H, f))

    results = []

    # ---- A1 各格互不雷同 ----
    # 只认图面：取每格格心一小片，两两比色差。同一构图被复制到两格时色差极小，
    # 这是「几格其实是同一张」最直接的证据。格数本身不必在这里再数一遍——A3 从
    # 图面（格心采样）兜、A5 从源图（KF01..KF0N 齐全）兜，再数一遍只是重复。
    if args.layout == "table":
        _cols, _rows, _cw, _ih2, _ch, _step2, _pad2 = table_geometry(args.expect, f)
        _rg2 = int(T_ROW_GAP * f)
        _rw = W - _pad2 * 2
        centers = []
        for r in range(_rows):
            rn = min(_cols, args.expect - r * _cols)          # 本行实际格数
            _row_w = rn * _cw + (rn - 1) * _step2
            _x0 = _pad2 + (_rw - _row_w) // 2                  # 每行各自居中
            for c in range(rn):
                centers.append((_x0 + c * (_cw + _step2) + _cw / 2,
                                T_BOARD_Y * f + r * (_ch + _rg2) + _ih2 / 2))
    else:
        _gw2, _gh2, _gap2 = raw_grid_geometry(W, grid_of(args.expect)[0])
        _cols, _rows = grid_of(args.expect)
        _tw, _th = _gw2 * _cols + _gap2 * (_cols + 1), _gh2 * _rows + _gap2 * (_rows + 1)
        _ox, _oy = (W - _tw) // 2, (H - _th) // 2
        centers = [(_ox + _gap2 + c * (_gw2 + _gap2) + _gw2 / 2,
                    _oy + _gap2 + r * (_gh2 + _gap2) + _gh2 / 2)
                   for r in range(_rows) for c in range(_cols)]
    centers = centers[:max(1, min(args.expect, 6))]
    _r2 = max(6, int(18 * f))
    patches = [patch_rgb(img, int(cx), int(cy), _r2) for cx, cy in centers]
    mind, pair = 999.0, None
    for i in range(len(patches)):
        for j in range(i + 1, len(patches)):
            dd = dist(patches[i], patches[j])
            if dd < mind:
                mind, pair = dd, (i + 1, j + 1)
    ok1 = pair is not None and mind >= 12.0
    detail1 = ("最小色差 %.0f/12（最近一对：第%d格 vs 第%d格）" % (mind, pair[0], pair[1])
               if pair else "格数不足，无法比对")
    results.append(line("A1", "%d 格互不雷同" % len(patches), detail1, ok1))

    # ---- A4 整张画幅 ----
    if args.layout == "table":
        exp_h = table_height(args.expect, f)
        ok = abs(W - int(T_W * f)) <= T_W * f * 0.03 and abs(H - exp_h) <= exp_h * 0.02
        detail = "%dx%d (期望宽 %d、高 %d±2%%，按 %d 格复算)" % (
            W, H, int(T_W * f), exp_h, args.expect)
    else:
        # raw 版不评整张比例（格宽随列数变，2×2 时画布必然更高），只核宽度基准与网格装得下
        gw4, gh4, gap4 = raw_grid_geometry(W, grid_of(args.expect)[0])
        cols4, rows4 = grid_of(args.expect)
        fits4 = (gw4 * cols4 + gap4 * (cols4 + 1) <= W
                 and gh4 * rows4 + gap4 * (rows4 + 1) <= H)
        ok = abs(W - int(RAW_W * f)) <= RAW_W * f * 0.03 and fits4
        detail = "%dx%d 比例 %.4f；网格 %dx%d 装得下 %s" % (
            W, H, ratio(W, H), cols4, rows4, "是" if fits4 else "否")
    results.append(line("A4", "整张画幅", detail, ok))

    # ---- A2 格内画面区比例 ----
    if args.layout == "table":
        _c2, _r2, cw2, ch2, _h2, _s2, _p2 = table_geometry(args.expect, f)
    else:
        cw2, ch2, _g = raw_grid_geometry(W, grid_of(args.expect)[0])
    cell_ratio = ratio(cw2, ch2)
    ok2 = abs(cell_ratio - TARGET_RATIO) <= 0.01
    results.append(line("A2", "格内画面区",
                        "%dx%d 比例 %.4f (应 %.4f)" % (cw2, ch2, cell_ratio, TARGET_RATIO), ok2))

    # ---- A6 题头带 ----
    if spec["header"]:
        mean, sd = band_stats(img, int(H * 0.01), int(T_HEADER * f * 0.85))
        ok6 = mean < 130
        results.append(line("A6", "题头深色带",
                            "亮度 %.0f 标准差 %.1f（应<130，深色通栏）" % (mean, sd), ok6))
    else:
        # raw 版没有页眉：采样带严格取网格上方的留白。格数少时格变大、留白变窄
        # （2×2 只有约 20px），按整张比例取样会切进画面，画面本身的标准差会被
        # 误判成「顶部有文字」，所以留白高度按几何复算，不按百分比。
        _gw5, _gh5, _gap5 = raw_grid_geometry(W, grid_of(args.expect)[0])
        _c5, _r5 = grid_of(args.expect)
        _oy5 = (H - (_gh5 * _r5 + _gap5 * (_r5 + 1))) // 2
        top = max(4, _oy5 - 2)
        mean, sd = band_stats(img, 0, top)
        ok6 = sd < 12
        results.append(line("A6", "无页眉(零文字)",
                            "顶部%dpx 标准差 %.1f（应<12，说明无文字）" % (top, sd), ok6))

    # ---- A3 结构 ----
    if spec["grid"]:
        cols, rows = grid_of(args.expect)
        gw, gh, gap = raw_grid_geometry(W, cols)
        grid_w, grid_h = gw * cols + gap * (cols + 1), gh * rows + gap * (rows + 1)
        fits = gw > 0 and grid_w <= W and grid_h <= H
        ok3 = fits and abs(ratio(gw, gh) - TARGET_RATIO) <= 0.005
        results.append(line("A3", "网格 %d列x%d行" % (cols, rows),
                            "格%dx%d 比例%.4f (应%.4f) 网格%dx%d 画布%dx%d"
                            % (gw, gh, ratio(gw, gh), TARGET_RATIO, grid_w, grid_h, W, H), ok3))
    else:
        # 按已知几何复算，再到预期位置采样：格心应有画面，格间应是底色
        base = patch_rgb(img, int(W - 30), int(H - 30), 10)
        cols, rows, cw, ih, ch, step, pad = table_geometry(args.expect, f)
        rg = int(T_ROW_GAP * f)
        rw = W - pad * 2
        board_y = T_BOARD_Y * f
        hit, miss, gaps = 0, 0, 0
        for r in range(rows):
            rn = min(cols, args.expect - r * cols)
            row_w = rn * cw + (rn - 1) * step
            x0 = pad + (rw - row_w) // 2
            for c in range(rn):
                cx = x0 + c * (cw + step) + cw / 2
                cy = board_y + r * (ch + rg) + ih / 2
                if dist(patch_rgb(img, int(cx), int(cy)), base) > 25:
                    hit += 1
            for c in range(1, rn):
                gx = x0 + c * (cw + step) - step / 2
                gy = board_y + r * (ch + rg) + ih / 2
                gaps += 1
                if dist(patch_rgb(img, int(gx), int(gy)), base) < 14:
                    miss += 1
        ok3 = hit == args.expect and miss == gaps
        results.append(line("A3", "%d列x%d行 对齐未压边" % (cols, rows),
                            "格心有画面 %d/%d，格间为底色 %d/%d"
                            % (hit, args.expect, miss, gaps), ok3))

    # ---- A7 ④ 画面带（仅 table；raw 版没有六区分带，不评此项）----
    if args.layout == "table":
        cols, rows, cw, ih, ch, step, pad = table_geometry(args.expect, f)
        rg = int(T_ROW_GAP * f)
        prof = row_profile(img)
        board_y = T_BOARD_Y * f
        y0 = int((T_BAND_Y + T_BAND_H) * f)
        board_bottom = board_y + ch * rows + rg * (rows - 1)
        y1 = int(min(H, board_bottom + int(90 * f)))
        found = bands(prof, 22, int(60 * f), y0, y1)
        exp_h = ih
        exp_tops = [board_y + r * (ch + rg) for r in range(rows)]
        tol_y = H * 0.02
        tall = [(a, b) for a, b in found if abs((b - a) - exp_h) <= exp_h * 0.10]
        hits = sum(1 for et in exp_tops
                   if any(abs(a - et) <= tol_y and abs((b - a) - exp_h) <= exp_h * 0.10
                          for a, b in tall))
        ok7 = hits == rows
        results.append(line("A7", "%d 行画面带" % rows,
                            "检出%d条 %s；顶边落在预期位置的 %d/%d（目标高≈%d）"
                            % (len(found), found[:4], hits, rows, int(exp_h)), ok7))

    # ---- A5 单格源图 ----
    if args.cells:
        cdir = os.path.abspath(args.cells)
        if not os.path.isdir(cdir):
            results.append(line("A5", "源图 16:9", "目录不存在: %s" % cdir, False))
        else:
            pat = re.compile(r"^(P\d\d)-KF(\d+)\.png$", re.I)
            found = {}
            for fn in sorted(os.listdir(cdir)):
                m = pat.match(fn)
                if not m:
                    continue
                if args.prefix and m.group(1).upper() != args.prefix.upper():
                    continue
                found[int(m.group(2))] = os.path.join(cdir, fn)
            sizes, bad = set(), []
            for k, fp in found.items():
                s = Image.open(fp).size
                sizes.add(s)
                if abs(ratio(*s) - TARGET_RATIO) > RATIO_TOL:
                    bad.append(os.path.basename(fp))
            complete = len(found) == args.expect and sorted(found) == list(range(1, args.expect + 1))
            uniform = len(sizes) <= 1
            detail = "%d/%d 齐全  尺寸%s  %s" % (
                len(found), args.expect,
                "一致 %dx%d" % next(iter(sizes)) if (sizes and uniform) else "不一致",
                ("比例异常:" + ",".join(bad)) if bad else "比例均 16:9")
            results.append(line("A5", "源图 16:9", detail, complete and uniform and not bad))

    # ---- 统一按 A1→A7 顺序打印 ----
    flush_rows()

    # ---- 可选：按几何裁出单格（仅 raw）----
    if args.crop_to and spec["grid"]:
        outdir = os.path.abspath(args.crop_to)
        os.makedirs(outdir, exist_ok=True)
        gw, gh, gap = raw_grid_geometry(W, grid_of(args.expect)[0])
        cols, rows = grid_of(args.expect)
        n = max(1, min(args.expect, 6))
        grid_w, grid_h = gw * cols + gap * (cols + 1), gh * rows + gap * (rows + 1)
        ox, oy = (W - grid_w) // 2, (H - grid_h) // 2
        for i in range(n):
            r, c = divmod(i, cols)
            x = ox + gap + c * (gw + gap)
            y = oy + gap + r * (gh + gap)
            fp = os.path.join(outdir, "%s-KF%02d.png" % (args.prefix or "P01", i + 1))
            img.crop((x, y, x + gw, y + gh)).save(fp)
            print("  [裁出] %s" % fp)

    passed = sum(1 for r in results if r)
    total = len(results)
    print("  " + "-" * 76)
    print("  汇总：%s（%d/%d）\n" % ("PASS" if passed == total else "FAIL", passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
