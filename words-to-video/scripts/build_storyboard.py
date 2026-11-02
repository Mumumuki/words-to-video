# -*- coding: utf-8 -*-
"""
build_storyboard.py —— 按 SB-STYLE 版式规范合成故事板（S12-b 出图与排版）

每段输出两版式（--layout 选择，或 all 一次出两张）：

  table  段落板（给人看）：六区竖幅制作板，2400×2960（约 4:5）。
         ① 出场人物 / ② 对手戏场景 / ③ 空间调度 / ④ 分镜关键帧 /
         ⑤ 光影与材质 / ⑥ 摄影与技术说明。
         叙事优先：非专业者不必懂景别运镜，也能读懂这一段在演什么。

  raw    模型版（给视频模型）：2×3 网格、每格严格 16:9、零文字零页眉页脚，
         2352×1000。裁开即 6 张图生视频首帧。

配色按风格卡 palette 上色（见 templates/style-palette.md）。
标题字体按时代美学取向，通过 --art-font 传入。

数据 JSON 结构（每张故事板一份，除 cells 外全部字段可缺省）：
  {
    "title": "《篇名》", "para": "P01", "tc": "00:00.000–00:15.000",
    "sb": "SB-01", "style": "风格卡版本", "total": 2, "index": 1,
    "ep": "情节1", "seg": "段落名",
    "subtitle": "副行：篇名 · 地点 · 主题",
    "emotion_arc": "孤寂 · 思乡",
    "bilingual": true,
    "cast":  [{"id":"角色01-造型A","name":"游子","note":"六镜全程在场",
               "crop":[l,t,r,b],"cutout":true,"shadow":true}],
    "props": [{"id":"道具01","name":"矮榻","note":"镜 01–02 卧处",
               "crop":[l,t,r,b],"cutout":true}],
    "set":   {"id":"场景01-V02","name":"客舍内室 · 人眼全景","note":"全段唯一取景视角",
               "crop":[l,t,r,b]},
    "blocking": {"shape":"rect","w":4.2,"h":3.0,
                 "actors":[{"tag":"A","x":0.3,"y":0.5,"name":"游子"}],
                 "relations":[{"from":"A","to":"B","type":"gaze"}],
                 "cam":[0.5,0.92],
                 "note":"整段无位移，机位绕榻侧拍"},
    "materials": [{"label":"月光","note":"窗棂切光 · 冷 5600K","cell":1}],
    "tech": [{"k":"画幅","v":"2.39:1"}],
    "cells": [ ... 恰好 6 项 ... ]
  }

资产图自动按编号在 --assets 目录里找：
  character-<cast.id>*.png / prop-<props.id>*.png / scene-<set.id>*.png
找不到则该格降级为纯文字胶囊并在 stderr 打印告警（不再静默）；
crop 为归一化 [l,t,r,b]。

**资产文件命名约定（一条卡一个文件，文件名里用卡内主编号）**：
  character-角色01-造型A.png     角色卡（6:5，五区）
  scene-场景01.png               场景卡（6:5，左二右四）——用场景主编号，不带视角子编号
  prop-道具01.png                道具卡（5:6，四宫格）
数据里 `set.id` 仍写视角子编号（`场景01-V02`，用于图上标注与提示词引用），
脚本找不到 `scene-场景01-V02*` 时自动回退到 `scene-场景01*`。

crop 缺省值：
  cast  缺省取角色卡左侧半身主视觉区（CHAR_MAIN_CROP，已是头顶到腰胯），不再二次裁切；
        若你的图是外部上传的单张全身人像，请显式给 crop（如 [0,0,1,1] 表示整张）。
  props 缺省取道具卡「正面」格（PROP_DEFAULT_CROP，按 1500×1800 卡面实算，已让开格内左上标签）——
        四宫格整张中心裁切会切到格线与说明条。
  set   缺省取场景卡左下格 V02 人眼视角（SCENE_MAIN_CROP，按 1800×1500 卡面实算，已让开格内左上标签）——
        六格整张裁切会把中缝、格框与右列「远景N · V0n」标签一起裁进 ② 区。

人物与道具默认做白底去背（cutout，默认 true；场景不做）：
  只删「与画布四边连通的近白区域」，人物自身的白衣、白发、白袖不会被挖空。
  去背成功后自动裁到内容边界，按底部对齐贴进版面并补一层接触阴影，看起来
  是「立在纸上」而不是「贴了张白底方块」。原图不是白底时自动放弃去背，退回
  带框裁切，不会出空白格。资产图最好在 S9–S11 就出纯白底、无投影、无文字。

cast 支持 1–3 个主要角色，按人数自动换排法：
  1 人   半身大图 + 右侧文字说明（角色卡只有半身主视觉与遮脸三视图，没有全身图可切）
  2–3 人 等高半身像并排，姓名前带 A/B/C 圆标，与 ③ 空间调度图的方位点对应；
         道具同时退成一行文字，把版面让给人物。
  超过 3 人只排前三位，其余提示「见第一部分角色卡」。
  半身像一律不画接触阴影（腰胯断面加地面阴影会像悬空）。

一个段落只对应一个场景：② 区只放 `set` 指定的那一个视角，③ 区调度图也只按
该场景绘制。段落跨两个场景时，换景在 cells 上体现，不改本 JSON 结构。

③ 空间调度图按需画这几样东西，缺字段就自动不画：
  blocking.actors     站位点（tag/x/y/name），坐标为场地归一化值（0 为左/上，1 为右/下）
  blocking.relations  关系线（type: gaze 视线 / move 位移 / axis 轴线）
  blocking.cam        机位方块，归一化坐标 [x,y]（如 [0.5,0.92] 表示场地中轴靠下机位），
                      并画一条到首位角色的取景虚线；单人静态段也建议给，能交代「谁在看谁」
  blocking.w / h      场地实际尺寸（米），用于画比例尺
  blocking.note       调度说明，图下一至三行
单人段没有 relations 时只画人位、机位与场地框，不画关系线。

用法：
  python scripts/build_storyboard.py --data sb01.json --cells cells --assets assets --out sb01.png --layout all
  python scripts/build_storyboard.py --batch boards --cells cells --assets assets --outdir . --layout table

依赖：Pillow（pip install pillow），可选 numpy（去背需要，缺省时自动跳过）。
"""
import os
import sys
import json
import glob
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    import numpy as np
except ImportError:
    np = None

# ---------------- 配色（取自 templates/style-palette.md，按风格卡 palette 上色） ----------------
DEFAULT_PALETTE = {
    "base":       (245, 245, 245),
    "band":       (232, 232, 232),
    "rule":       (60, 60, 60),
    "rule-heavy": (68, 68, 68),
    "ink":        (40, 40, 40),
    "ink2":       (70, 70, 70),
    "ink3":       (110, 110, 110),
    "ink4":       (140, 140, 140),
    "sep":        (200, 200, 200),
    "num-stroke": (40, 40, 40),
    "accent":     (176, 106, 60),
}
PALETTE = dict(DEFAULT_PALETTE)


def load_palette(path):
    with open(path, encoding="utf-8") as _fh:
        PALETTE.update({k: tuple(v) for k, v in json.load(_fh).items()})


C_BG = PALETTE["base"]
C_BAND = PALETTE["band"]
C_INK = PALETTE["ink"]
C_INK2 = PALETTE["ink2"]
C_INK3 = PALETTE["ink3"]
C_INK4 = PALETTE["ink4"]
C_FRAME = PALETTE["rule"]
C_DIV = PALETTE["rule"]
C_SEP = PALETTE["sep"]
C_NUM_STROKE = PALETTE["num-stroke"]
C_ACCENT = PALETTE["accent"]

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
# 艺术字候选：按时代美学取向由 --art-font 覆盖（见 style-palette.md §二）
ART_FONT_CANDIDATES = [
    "C:/Windows/Fonts/STZHONGS.TTF",
    "C:/Windows/Fonts/STSONG.TTF",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]

FONT_PATH = None
ART_PATH = None
_FONT_CACHE = {}


def find_font(preferred=None, cands=None):
    for p in ([preferred] if preferred else []) + (cands or FONT_CANDIDATES):
        if p and os.path.exists(p):
            return p
    return None


def font(size, art=False):
    """带缓存的字体加载。art=True 取艺术字体。"""
    size = max(8, int(size))
    key = (size, art)
    if key not in _FONT_CACHE:
        path = ART_PATH if art else FONT_PATH
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]


def text_w(d, text, fnt):
    return d.textlength(text, font=fnt)


def draw_text(d, xy, text, fnt, fill, anchor="lt", stroke_width=0, stroke_fill=None):
    kw = {"font": fnt, "fill": fill, "anchor": anchor}
    if stroke_width:
        kw["stroke_width"] = stroke_width
        kw["stroke_fill"] = stroke_fill or (0, 0, 0)
    d.text(xy, text, **kw)


def draw_tracked(d, xy, text, fnt, fill, tracking=0, anchor_left=True):
    """逐字绘制以实现字距（PIL 无原生 tracking）。返回绘制总宽。"""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += text_w(d, ch, fnt) + tracking
    return x - xy[0]


NOSTART = "，。、；：？！）」』】〕”’°%‰·…"


def wrap_cjk(d, text, fnt, max_w):
    """CJK 逐字累加，超宽折行；带行首禁则（标点、单位不落在行首）。"""
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if text_w(d, test, fnt) > max_w and cur:
            if ch in "°%‰":
                k = len(cur)
                while k > 1 and (cur[k - 1].isdigit() or cur[k - 1] == "."):
                    k -= 1
                if k < len(cur):
                    lines.append(cur[:k])
                    cur = cur[k:] + ch
                    continue
            if ch in NOSTART and len(cur) > 1:
                lines.append(cur[:-1])
                cur = cur[-1] + ch
            else:
                lines.append(cur)
                cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def fit_crop(img, tw, th):
    """保持比例中心裁切到目标 (tw, th)，再缩放。避免拉伸变形。"""
    sw, sh = img.size
    src_r, tgt_r = sw / float(sh), tw / float(th)
    if src_r > tgt_r:
        nw = int(sh * tgt_r)
        img = img.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    elif src_r < tgt_r:
        nh = int(sw / tgt_r)
        img = img.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return img.resize((max(1, tw), max(1, th)))


# 道具卡为 5:6 四宫格（1500×1800：顶栏 110、四格 712、说明条 44、底栏 60）。
# ① 区取图只取「正面」格，并避开左上角标签与格的边框。标签贴在格内 top 5px，在
# 1500 宽卡上占 y 约 0.105–0.118（y0 取 0.105 会把标签一起抠进图里）；正面格底边
# 在 y 约 0.473（852/1800），y1 取到 0.475 会带进一截格框，去背判据因此不过。
PROP_DEFAULT_CROP = [0.05, 0.12, 0.485, 0.468]

# 角色卡为 6:5 五区（1920×1600）：顶栏 7.2% / 上半区约 59.8%（左 25% 半身主视觉、
# 右 75% 三视图）/ 2px 分割线 / 下半区 33%（左 30% 六行信息表、右 70% 四格特写）。
# 左侧主视觉区已是「头顶到腰胯」，取图后不再二次裁切；y1 收在 0.615——
# 上半区底边（含那条 2px 通栏分割线）在 0.628 附近，取 0.66 会把分割线连同
# 下半区信息表首行一起裁进 ① 区。
CHAR_MAIN_CROP = [0.02, 0.08, 0.26, 0.615]

# 场景卡为 6:5 左二右四（1800×1500）：顶栏 96 / 左列 1120（上格 V01、下格 V02 人眼视角、
# 各约 1120×605）/ 中缝 30 / 右列 602 四格 / 底栏 48。
# ② 区只取左下格 V02 人眼写实全景，并让出格内左上角标签（标签贴格顶，在卡面
# y 约 0.523–0.556）；不取整卡——整卡会把中缝、格框与「远景N · V0n」标签一起裁进画面。
# 取值按模板渲染实测：V02 格 x 0.014–0.634、y 0.523–0.935，四边各内缩一点。
SCENE_MAIN_CROP = [0.03, 0.558, 0.63, 0.93]

# 已告警过的资产编号，避免同一张图重复刷屏
_WARNED = set()


def _warn(msg):
    if msg in _WARNED:
        return
    _WARNED.add(msg)
    sys.stderr.write("[warn] %s\n" % msg)


def find_asset(assets_dir, prefix, ident):
    """按编号在资产目录里找图：<prefix>-<ident>*.png。找不到返回 None。

    场景卡的编号是场景主编号（`场景01`），而数据里的引用写的是视角子编号
    （`场景01-V02`），因此 scene 找不到精确匹配时退一步用主编号再找一次。
    找不到会打一条告警——静默降级会让 ② 区无声地变成空底色。
    """
    if not assets_dir or not ident or not os.path.isdir(assets_dir):
        return None
    cands = [ident]
    if prefix == "scene" and "-" in ident:
        cands.append(ident.split("-")[0])
    for cid in cands:
        pat = os.path.join(assets_dir, "%s-%s*" % (prefix, cid))
        for p in sorted(glob.glob(pat)):
            if p.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                return p
    _warn("未找到资产图 %s-%s*.png（%s 将降级为占位）"
          % (prefix, ident, os.path.basename(assets_dir) or "assets"))
    return None


def load_asset(path, crop=None, keep_alpha=False):
    im = Image.open(path)
    im = im.convert("RGBA") if keep_alpha else im.convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h),
                      int(crop[2] * w), int(crop[3] * h)))
    return im


# ---------------- 白底去背（人物 / 道具） ----------------
def _dilate(mask):
    p = np.pad(mask, 1, constant_values=False)
    return (p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1]
            | p[1:-1, :-2] | p[1:-1, 2:])


def _erode(mask):
    # 画布外一律视为背景，边缘像素才不会被误腐蚀
    p = np.pad(mask, 1, constant_values=True)
    return (p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1]
            & p[1:-1, :-2] & p[1:-1, 2:])


def _line_sweep(mask):
    """从画布四边做直线连续段扫描，得到第一轮「外部背景」候选。"""
    left = np.logical_and.accumulate(mask, axis=1)
    right = np.logical_and.accumulate(mask[:, ::-1], axis=1)[:, ::-1]
    up = np.logical_and.accumulate(mask, axis=0)
    down = np.logical_and.accumulate(mask[::-1, :], axis=0)[::-1, :]
    return left | right | up | down


def keyout_white(rgb, tol=26.0, feather=2.0, edge=6):
    """白底键控去背，返回 RGBA；不适合去背时返回 None。

    只删「与画布四边连通的近白区域」——人物身上的白袍、白发、白袖不与边缘
    连通，因而完整保留。原图不是白底（边缘采样几乎不白）或去背后没有内容时
    返回 None，由调用方退回带框裁切。
    """
    if np is None:
        return None
    if rgb.mode == "RGBA":                               # 已是透明底，直接用
        a0 = np.asarray(rgb.getchannel("A"))
        if (a0 < 250).mean() > 0.02:
            return rgb
    rgb = rgb.convert("RGB")
    a = np.asarray(rgb).astype(np.float32)
    h, w, _ = a.shape
    if h < 16 or w < 16:
        return None
    e = max(2, min(edge, h // 8, w // 8))
    k = max(4, int(min(h, w) * 0.07))
    corners = np.stack([a[:k, :k].reshape(-1, 3).mean(axis=0),
                        a[:k, -k:].reshape(-1, 3).mean(axis=0),
                        a[-k:, :k].reshape(-1, 3).mean(axis=0),
                        a[-k:, -k:].reshape(-1, 3).mean(axis=0)])
    # 四角散度：纯色设定图 <3，实景画面 >40。花杂的一律不去背。
    if float(np.linalg.norm(corners - corners.mean(axis=0), axis=1).max()) > 12.0:
        return None
    white = corners.mean(axis=0)                         # 四角均值作白点，抗色偏
    border = np.concatenate([a[:e].reshape(-1, 3), a[-e:].reshape(-1, 3),
                             a[:, :e].reshape(-1, 3), a[:, -e:].reshape(-1, 3)])
    near = np.linalg.norm(a - white, axis=2) < tol
    if (np.linalg.norm(border - white, axis=1) < tol).mean() < 0.55:
        return None                                      # 边框大半不是底色
    bg = _line_sweep(near)
    for _ in range(3):                                   # 补拐角与凹处
        bg = bg | (_dilate(bg) & near)
    cov = 1.0 - bg.mean()
    if cov < 0.04 or cov > 0.985:                        # 去背无效
        return None
    alpha = np.where(_erode(bg), 0, 255).astype(np.uint8)
    aim = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(feather))
    out = rgb.convert("RGBA")
    out.putalpha(aim)
    return out


def trim_alpha(rgba, thresh=16):
    """按 alpha 包围盒裁到内容边界，去掉去背后残留的透明留白。"""
    if np is None or rgba is None:
        return rgba
    a = np.asarray(rgba.getchannel("A"))
    ys, xs = np.where(a > thresh)
    if len(xs) == 0:
        return None
    return rgba.crop((int(xs.min()), int(ys.min()),
                      int(xs.max()) + 1, int(ys.max()) + 1))


def flatten(im, bg=(255, 255, 255)):
    """把带 alpha 的图压平到纯色底，避免透明区贴图变黑。"""
    if im.mode != "RGBA":
        return im
    c = Image.new("RGB", im.size, bg)
    c.paste(im, (0, 0), im)
    return c


def fit_contain(img, tw, th):
    """等比缩放到 (tw, th) 之内，不裁不拉伸。"""
    sw, sh = img.size
    k = min(tw / float(sw), th / float(sh))
    return img.resize((max(1, int(round(sw * k))), max(1, int(round(sh * k)))),
                      Image.LANCZOS)


def paste_cutout(base, rgba, box, align="bottom", shadow=True):
    """把透明底资产贴进 box：等比缩放、底部/居中对齐，可补一层接触阴影。"""
    x, y, w, h = [int(v) for v in box]
    pic = fit_contain(rgba, w, h)
    pw, ph = pic.size
    px = x + (w - pw) // 2
    py = y + (h - ph) if align == "bottom" else y + (h - ph) // 2
    if shadow and pw > 8:
        sw2 = int(pw * 0.58)
        sh2 = max(5, int(ph * 0.05))
        sm = Image.new("L", (sw2, sh2), 0)
        ImageDraw.Draw(sm).ellipse([0, 0, sw2 - 1, sh2 - 1], fill=124)
        sm = sm.filter(ImageFilter.GaussianBlur(max(2, int(sh2 * 0.5))))
        dark = Image.new("RGBA", (sw2, sh2), ink_of(C_INK, 0.38) + (255,))
        dark.putalpha(sm)
        base.paste(dark, (max(0, px + (pw - sw2) // 2),
                          max(0, py + ph - sh2 // 2)), dark)
    base.paste(pic, (max(0, px), max(0, py)), pic)
    return pic


def grid_of(n):
    """格数 → (列, 行)。2–3 格单行，4 格 2×2，5–6 格 3×2。

    格数按段落实际关键帧数走，不强凑 6 格：短段落（不足 10 秒的收束段、
    单动作段）常常只有 2–3 个关键帧，硬补到 6 格会造出没有戏剧依据的画面。
    """
    if n <= 3:
        return n, 1
    if n == 4:
        return 2, 2
    return 3, 2


def load_cells(data, cells_dir):
    cells = data["cells"]
    n = len(cells)
    if not 2 <= n <= 6:
        raise ValueError("cells 须为 2–6 项，实际 %d；1 格不成板，7 格以上应拆段" % n)
    imgs = []
    for i in range(n):
        p = os.path.join(cells_dir, "%s-KF%02d.png" % (data["para"], i + 1))
        if not os.path.exists(p):
            raise FileNotFoundError("缺少单格画面：%s" % p)
        imgs.append(Image.open(p).convert("RGB"))
    return cells, imgs


# ---------------- 绘制基元 ----------------
def circle_num(d, cx, cy, r, num, fill, ink, size, lw=0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=None if not lw else ink, width=lw)
    if isinstance(num, str):
        fnt = font(size, art=True)
    else:
        fnt = font(size)
    draw_text(d, (cx, cy + r * 0.02), str(num), fnt, ink, anchor="mm")


def gradient_text(img, xy, text, fnt, c_top, c_bot, stroke=None, sw=0):
    """竖向渐变填充的艺术字；先在画布上描边，再用渐变遮罩贴字面。"""
    x, y = int(xy[0]), int(xy[1])
    probe = ImageDraw.Draw(img)
    bbox = probe.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = max(4, int(sw * 2) + 4)
    W2, H2 = tw + pad * 2, th + pad * 2
    if stroke and sw:
        probe.text((x - bbox[0], y - bbox[1]), text, font=fnt, fill=stroke,
                   stroke_width=sw, stroke_fill=stroke)
    mask = Image.new("L", (W2, H2), 0)
    ImageDraw.Draw(mask).text((pad - bbox[0], pad - bbox[1]), text, font=fnt, fill=255)
    grad = Image.new("RGB", (W2, H2))
    gd = ImageDraw.Draw(grad)
    for yy in range(H2):
        t = yy / float(max(1, H2 - 1))
        gd.line([(0, yy), (W2, yy)],
                fill=tuple(int(c_top[i] + (c_bot[i] - c_top[i]) * t) for i in range(3)))
    img.paste(grad, (x - pad, y - pad), mask)


def ink_of(bg, ratio=0.10):
    """在给定底色上取一个极低对比的派生色（用于底纹大字）。"""
    return tuple(int(c + (255 - c) * ratio) for c in bg)


# ---------------- 段落板 · table（六区） ----------------
def build_table(data, cells_dir, out_path, f, assets_dir=None):
    """段落板（给人看）：六区竖幅制作板，2400×2960。

    ① 出场人物 / ② 对手戏场景 / ③ 空间调度 / ④ 分镜关键帧 /
    ⑤ 光影与材质 / ⑥ 摄影与技术说明。区块数与位置固定，无内容的区块自动省略内容不省略区。
    """
    def S(v):
        return int(v * f)

    W = S(2400)
    PAD = S(72)
    RW = W - PAD * 2                      # 内容宽 2256

    HEADER_H, GAP1 = S(200), S(44)
    BAND_H, GAP2 = S(720), S(40)
    SEC4T, ROW_GAP = S(100), S(40)
    GAP3, SEC56_H, FOOTER_H, BOTTOM = S(56), S(400), S(60), S(60)
    STEP = S(40)                          # 格间距；3 列时的原值，其余格数沿用

    n = len(data["cells"])
    cols, rows = grid_of(n)
    if cols == 3:
        CELL_W, CELL_IMG_H, CELL_H = S(725), S(408), S(620)   # 5–6 格沿用原几何
    else:
        CELL_W = (RW - STEP * (cols - 1)) // cols
        CELL_IMG_H = CELL_W * 9 // 16
        CELL_H = CELL_IMG_H + (S(620) - S(408))               # 信息区高度不变

    BOARD_H = CELL_H * rows + ROW_GAP * (rows - 1)
    H = (HEADER_H + GAP1 + BAND_H + GAP2 + SEC4T + BOARD_H
         + GAP3 + SEC56_H + FOOTER_H + BOTTOM)

    bilingual = bool(data.get("bilingual", False))
    cells, imgs = load_cells(data, cells_dir)

    img = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(img)

    # ================= 题头 =================
    d.rectangle([0, 0, W, HEADER_H], fill=C_INK)
    num = str(data.get("para", "P01")).lstrip("Pp").lstrip("0") or "1"
    num = num.zfill(2)

    # 左侧：小字栏目名 + 大号段落号（艺术字，竖向渐变）
    draw_text(d, (PAD, S(38)), "情 节", font(S(22)), ink_of(C_INK, 0.45))
    top_c = tuple(min(255, int(c + (255 - c) * 0.42)) for c in C_ACCENT)
    gradient_text(img, (PAD - S(6), S(72)), num, font(S(104), art=True), top_c, C_ACCENT)

    tx = PAD + S(212)
    draw_text(d, (tx, S(58)), data.get("title", ""), font(S(56), art=True), C_BG)
    draw_text(d, (tx, S(142)), data.get("subtitle", data.get("title", "")),
              font(S(26)), ink_of(C_INK, 0.55))

    # 右侧信息组（右对齐，从右往左排）
    meta = [
        ("时间码", data.get("tc", "")),
        ("镜头", "%d 格" % len(cells)),
        ("风格", data.get("style", "")),
        ("情绪", data.get("emotion_arc", "")),
    ]
    rx = W - PAD
    slot = S(250)
    for i, (label, val) in enumerate(meta):
        rx1 = W - PAD - (len(meta) - 1 - i) * slot
        draw_text(d, (rx1, S(58)), label, font(S(22)), ink_of(C_INK, 0.5), anchor="rt")
        draw_text(d, (rx1, S(100)), val, font(S(30)), C_BG, anchor="rt")

    d.line([(0, HEADER_H), (W, HEADER_H)], fill=C_ACCENT, width=max(1, S(3)))

    # ================= ①②③ 三栏 =================
    BAND_Y = HEADER_H + GAP1
    col1_w, col2_w = S(640), S(900)
    col3_w = RW - col1_w - col2_w - S(80)
    x1, x2, x3 = PAD, PAD + col1_w + S(40), PAD + col1_w + col2_w + S(80)
    head_y = BAND_Y

    def section_head(x, y, idx, zh, en):
        r = S(15)
        circle_num(d, x + r, y + S(20), r, idx, C_ACCENT, C_BG, S(20))
        tw = draw_text(d, (x + S(42), y + S(4)), zh, font(S(34)), C_INK)
        if bilingual and en:
            draw_text(d, (x + S(42), y + S(48)), en, font(S(19)), C_INK4)

    def dashed_v(x, y0, y1):
        step = S(10)
        yy = y0
        while yy < y1:
            d.line([(x, yy), (x, min(yy + step // 2, y1))], fill=C_SEP, width=max(1, S(1)))
            yy += step

    dashes_y0, dashes_y1 = BAND_Y + S(10), BAND_Y + BAND_H - S(10)

    # ---- ① 出场人物 + 登场道具 ----
    section_head(x1, head_y, "1", "出场人物", "CHARACTER")
    cast = data.get("cast") or []
    props = data.get("props") or []
    py = BAND_Y + S(96)
    n_cast = min(len(cast), 3)
    multi = n_cast >= 2
    # 半身取图：角色卡的左侧主视觉区本身就是「头顶到腰胯」，因此不再二次裁切；
    # 旧版在这里再切 56%，落到胸口，与「自头顶取到腰胯」不符。

    def cast_tag(i, c):
        """与 ③ 调度图的 A/B/C 对齐；对不上就按出场顺序给。"""
        for a in ((data.get("blocking") or {}).get("actors") or []):
            if a.get("name") and a.get("name") == c.get("name"):
                return str(a.get("tag", "")) or "ABC"[i]
            if a.get("id") and a.get("id") == c.get("id"):
                return str(a.get("tag", "")) or "ABC"[i]
        return "ABC"[i] if i < 3 else str(i + 1)

    def draw_cast(c, box, shadow=False):
        x, y, w, h = [int(v) for v in box]
        cp = find_asset(assets_dir, "character", c.get("id"))
        if cp:
            crop = c.get("crop")
            if crop is None:
                crop = CHAR_MAIN_CROP      # 角色卡左侧半身主视觉区（已是头顶到腰胯）
            pic = load_asset(cp, crop, keep_alpha=True)
            cut = trim_alpha(keyout_white(pic) if c.get("cutout", True) else None)
            if cut:
                # 半身像底下不画接触阴影，否则像悬在空中；整张全身图才需要
                paste_cutout(img, cut, (x, y, w, h), align="bottom", shadow=shadow)
            else:
                # 去背判据不过就会落到这里：出来是一块带框白底，属 B17 明令禁止的结果，
                # 不能静默——必须让人知道该回去检查 crop 区里是不是混进了文字或格线。
                if c.get("cutout", True):
                    _warn("角色图 %s 去背失败（白底三判据任一未过），①区已退回带框裁切；"
                          "请检查 crop 区四角是否留有纯色空白、区内是否混入标题文字或格线"
                          % os.path.basename(cp))
                img.paste(fit_crop(flatten(pic), w, h), (x, y))
                d.rectangle([x, y, x + w - 1, y + h - 1],
                            outline=C_FRAME, width=max(1, S(1)))
        else:
            d.rectangle([x, y, x + w - 1, y + h - 1],
                        fill=C_BAND, outline=C_SEP, width=max(1, S(1)))
            draw_text(d, (x + w // 2, y + h // 2), "待补", font(S(22)), C_INK4, anchor="mm")

    if cast:
        if multi:
            gap = S(22)
            slot = (col1_w - gap * (n_cast - 1)) // n_cast
            ih = S(270)
            for i, c in enumerate(cast[:3]):
                cx = x1 + i * (slot + gap)
                draw_cast(c, (cx, py, slot, ih))
                ty = py + ih + S(16)
                r = S(13)
                circle_num(d, cx + r, ty + S(17), r, cast_tag(i, c), C_ACCENT, C_BG, S(17))
                draw_text(d, (cx + r * 2 + S(10), ty), c.get("name", ""),
                          font(S(28), art=True), C_INK)
                draw_text(d, (cx, ty + S(40)), c.get("id", ""), font(S(17)), C_ACCENT)
                ny = ty + S(68)
                for ln in wrap_cjk(d, c.get("note", ""), font(S(19)), slot)[:2]:
                    draw_text(d, (cx, ny), ln, font(S(19)), C_INK3)
                    ny += S(26)
            if len(cast) > 3:
                draw_text(d, (x1, py + S(270) + S(150)),
                          "另有 %d 名次要角色，见第一部分角色卡" % (len(cast) - 3),
                          font(S(18)), C_INK4)
        else:
            c0 = cast[0]
            # 单人同样用半身大图：角色卡里只有半身主视觉与被灰圆遮脸的三视图，
            # 没有可用的全身图；硬切三视图会得到一张没有脸的人像。
            cw, chh = S(210), S(330)
            draw_cast(c0, (x1, py, cw, chh), shadow=c0.get("shadow", False))
            tx0 = x1 + cw + S(26)
            draw_text(d, (tx0, py + S(6)), c0.get("name", ""), font(S(34), art=True), C_INK)
            draw_text(d, (tx0, py + S(52)), c0.get("id", ""), font(S(21)), C_ACCENT)
            ny = py + S(96)
            for ln in wrap_cjk(d, c0.get("note", ""), font(S(23)), x1 + col1_w - tx0)[:4]:
                draw_text(d, (tx0, ny), ln, font(S(23)), C_INK2)
                ny += S(34)
    else:
        draw_text(d, (x1, py), "本段无出场人物", font(S(23)), C_INK4)

    # 道具：单人给图；人多退成一行文字，把版面让给人物
    dy = BAND_Y + (S(520) if multi else S(440))
    d.line([(x1, dy), (x1 + col1_w, dy)], fill=C_SEP, width=max(1, S(1)))
    draw_text(d, (x1, dy + S(16)), "登场道具", font(S(24)), C_INK)
    if props and multi:
        ny = dy + S(54)
        for p in props[:3]:
            txt = p.get("name", "") + (" · " + p.get("note", "") if p.get("note") else "")
            for ln in wrap_cjk(d, txt, font(S(20)), col1_w)[:2]:
                draw_text(d, (x1, ny), ln, font(S(20)), C_INK3)
                ny += S(28)
    elif props:
        px, pw = x1, S(145)
        for p in props[:2]:
            ty0 = dy + S(56)
            pp = find_asset(assets_dir, "prop", p.get("id"))
            if pp:
                pic = load_asset(pp, p.get("crop") or PROP_DEFAULT_CROP, keep_alpha=True)
                cut = keyout_white(pic) if p.get("cutout", True) else None
                cut = trim_alpha(cut)
                if cut:
                    # 与下面的带框分支同为 pw×pw：去背成功与失败若尺寸不同，
                    # 同一个道具在不同段落里会一大一小地跳。
                    paste_cutout(img, cut, (px, ty0, pw, pw),
                                 align="bottom", shadow=p.get("shadow", True))
                else:
                    if p.get("cutout", True):
                        _warn("道具图 %s 去背失败（白底三判据任一未过），①区已退回带框裁切"
                              % os.path.basename(pp))
                    img.paste(fit_crop(flatten(pic), pw, pw), (px, ty0))
                    d.rectangle([px, ty0, px + pw - 1, ty0 + pw - 1],
                                outline=C_FRAME, width=max(1, S(1)))
            else:
                d.rectangle([px, ty0, px + pw - 1, ty0 + pw - 1],
                            fill=C_BAND, outline=C_SEP, width=max(1, S(1)))
            draw_text(d, (px, ty0 + pw + S(10)), p.get("name", ""), font(S(22)), C_INK)
            ny = ty0 + pw + S(40)
            for ln in wrap_cjk(d, p.get("note", ""), font(S(19)), pw)[:2]:
                draw_text(d, (px, ny), ln, font(S(19)), C_INK4)
                ny += S(26)
            px += pw + S(20)
    elif not props:
        draw_text(d, (x1, dy + S(56)), "本段无道具", font(S(21)), C_INK4)

    dashed_v(x1 + col1_w + S(20), dashes_y0, dashes_y1)

    # ---- ② 对手戏场景 ----
    section_head(x2, head_y, "2", "对手戏场景", "ENVIRONMENT")
    st = data.get("set") or {}
    iy = BAND_Y + S(96)
    iw = col2_w - S(80)
    ih = int(iw * 9.0 / 16.0)
    sp = find_asset(assets_dir, "scene", st.get("id"))
    if sp:
        # 缺省取 V02 人眼视角格；不取整卡，否则会把中缝与右列标签裁进 ② 区
        scrop = st.get("crop") or SCENE_MAIN_CROP
        img.paste(fit_crop(load_asset(sp, scrop), iw, ih), (x2 + S(40), iy))
        d.rectangle([x2 + S(40), iy, x2 + S(40) + iw - 1, iy + ih - 1], outline=C_FRAME, width=max(1, S(1)))
    else:
        d.rectangle([x2 + S(40), iy, x2 + S(40) + iw - 1, iy + ih - 1], fill=C_BAND, outline=C_SEP, width=max(1, S(1)))
        draw_text(d, (x2 + col2_w // 2, iy + ih // 2), st.get("name", "待补"), font(S(24)), C_INK4, anchor="mm")
    ty = iy + ih + S(24)
    tx2 = x2 + S(40)
    draw_text(d, (tx2, ty), st.get("name", ""), font(S(30), art=True), C_INK)
    draw_text(d, (tx2, ty + S(42)), st.get("id", ""), font(S(21)), C_ACCENT)
    ty += S(76)
    for ln in wrap_cjk(d, st.get("note", ""), font(S(23)), iw)[:2]:
        draw_text(d, (tx2, ty), ln, font(S(23)), C_INK2)
        ty += S(32)

    dashed_v(x2 + col2_w + S(20), dashes_y0, dashes_y1)

    # ---- ③ 空间调度 ----
    section_head(x3, head_y, "3", "空间调度", "BLOCKING")
    bky = BAND_Y + S(96)
    bk = data.get("blocking") or {}
    bw, bh = col3_w, S(360)
    bx0, by0, bx1, by1 = x3, bky, x3 + bw, bky + bh
    if bk.get("actors"):
        grid_c = tuple(int(C_SEP[i] * 0.25 + C_BAND[i] * 0.75) for i in range(3))
        d.rectangle([bx0, by0, bx1, by1], fill=C_BAND)
        for gx in range(1, 4):
            px = bx0 + bw * gx // 4
            d.line([(px, by0 + 1), (px, by1 - 1)], fill=grid_c, width=max(1, S(1)))
        for gy in range(1, 3):
            py2 = by0 + bh * gy // 3
            d.line([(bx0 + 1, py2), (bx1 - 1, py2)], fill=grid_c, width=max(1, S(1)))
        d.rectangle([bx0, by0, bx1, by1], outline=C_INK3, width=max(1, S(2)))

        pad_x, pad_y = S(56), S(56)
        ax0, ay0 = bx0 + pad_x, by0 + pad_y
        ax1, ay1 = bx1 - pad_x, by1 - pad_y

        def pt(a):
            return (ax0 + (ax1 - ax0) * float(a.get("x", 0.5)),
                    ay0 + (ay1 - ay0) * float(a.get("y", 0.5)))

        amap = {a.get("tag", str(i)): a for i, a in enumerate(bk["actors"])}
        # 关系线：同一对角色已有视线时不再叠画轴线（两者在影视语义上同为连线）
        rels = bk.get("relations", [])
        gaze_pairs = {(r.get("from"), r.get("to")) for r in rels if r.get("type") == "gaze"}
        for rel in rels:
            a, b = amap.get(rel.get("from")), amap.get(rel.get("to"))
            if not a or not b:
                continue
            kind = rel.get("type", "axis")
            if kind == "axis" and (rel.get("from"), rel.get("to")) in gaze_pairs:
                continue
            p, q = pt(a), pt(b)
            kind = rel.get("type", "axis")
            if kind == "gaze":
                d.line([p, q], fill=C_ACCENT, width=max(1, S(3)))
            elif kind == "move":
                d.line([p, q], fill=C_INK3, width=max(1, S(2)))
                arm = S(12)
                dx, dy = q[0] - p[0], q[1] - p[1]
                ln = max(1.0, (dx * dx + dy * dy) ** 0.5)
                ux, uy = dx / ln, dy / ln
                for sgn in (1, -1):
                    d.line([q, (q[0] - arm * (ux + sgn * uy * 0.5),
                                q[1] - arm * (uy - sgn * ux * 0.5))],
                           fill=C_INK4, width=max(1, S(2)))
            else:
                d.line([p, q], fill=C_INK4, width=max(1, S(2)))
                # 轴线：两端小竖杠
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                d.line([(mx, my - S(26)), (mx, my + S(26))], fill=C_INK4, width=max(1, S(1)))

        # 机位（可选）：实心方块 + 到主体的视线虚线
        cam = bk.get("cam")
        if cam:
            cxp = ax0 + (ax1 - ax0) * float(cam[0])
            cyp = ay0 + (ay1 - ay0) * float(cam[1])
            d.rectangle([cxp - S(13), cyp - S(10), cxp + S(13), cyp + S(10)], fill=C_INK3)
            draw_text(d, (cxp + S(19), cyp), "机位", font(S(18)), C_INK3, anchor="lm")
            if bk["actors"]:
                tp = pt(bk["actors"][0])
                dx, dy = tp[0] - cxp, tp[1] - cyp
                ln = max(1.0, (dx * dx + dy * dy) ** 0.5)
                ux, uy = dx / ln, dy / ln
                step, t = S(10), S(24)
                while t < ln - S(28):
                    d.line([(cxp + ux * t, cyp + uy * t),
                            (cxp + ux * min(t + step // 2, ln), cyp + uy * min(t + step // 2, ln))],
                           fill=C_INK4, width=max(1, S(1)))
                    t += step

        # 角色点
        r = S(26)
        for a in bk["actors"]:
            p = pt(a)
            fill = C_ACCENT if a.get("tag") == "A" else C_INK
            circle_num(d, int(p[0]), int(p[1]), r, a.get("tag", "?"), fill, C_BG, S(22))
            if a.get("name"):
                draw_text(d, (p[0], p[1] + r + S(6)), a["name"], font(S(20)), C_INK2, anchor="mt")

        # 比例尺
        if bk.get("w"):
            bar = S(120)
            sx0, sy = bx0 + S(20), by1 - S(26)
            d.line([(sx0, sy), (sx0 + bar, sy)], fill=C_INK3, width=max(1, S(2)))
            for ex in (sx0, sx0 + bar):
                d.line([(ex, sy - S(6)), (ex, sy + S(6))], fill=C_INK3, width=max(1, S(2)))
            draw_text(d, (sx0 + bar + S(10), sy), "%sm" % bk["w"], font(S(19)), C_INK3, anchor="lm")
        # 指北
        nx, ny = bx1 - S(34), by0 + S(34)
        d.line([(nx, ny + S(16)), (nx, ny - S(16))], fill=C_INK3, width=max(1, S(2)))
        d.polygon([(nx, ny - S(22)), (nx - S(7), ny - S(10)), (nx + S(7), ny - S(10))], fill=C_INK3)
        draw_text(d, (nx, ny - S(30)), "N", font(S(18)), C_INK3, anchor="mb")
    else:
        d.rectangle([bx0, by0, bx1, by1], fill=C_BAND, outline=C_SEP, width=max(1, S(1)))
        draw_text(d, (bx0 + bw // 2, by0 + bh // 2), "本段未填 blocking.actors",
                  font(S(22)), C_INK4, anchor="mm")
        # 单人段也应该有站位与机位；空着不是「无需调度」，多半是数据漏填
        _warn("blocking.actors 为空：③ 空间调度只能画成空框；单人段也请给出站位与 cam")

    ty = bky + bh + S(20)
    for ln in wrap_cjk(d, bk.get("note", ""), font(S(22)), bw)[:3]:
        draw_text(d, (x3, ty), ln, font(S(22)), C_INK2)
        ty += S(30)

    # ================= ④ 分镜关键帧 =================
    y4 = BAND_Y + BAND_H + GAP2
    d.line([(0, y4), (W, y4)], fill=C_DIV, width=max(1, S(1)))
    r4 = S(15)
    circle_num(d, PAD + r4, y4 + S(24), r4, "4", C_ACCENT, C_BG, S(20))
    draw_text(d, (PAD + S(42), y4 + S(6)), "分镜关键帧", font(S(34)), C_INK)
    if bilingual:
        draw_text(d, (PAD + S(42), y4 + S(52)), "STORYBOARD FRAMES", font(S(19)), C_INK4)
    seg = data.get("seg", "")
    rtxt = "段落 %s%s · %s" % (data.get("para", ""), (" " + seg) if seg else "", data.get("tc", ""))
    draw_text(d, (W - PAD, y4 + S(24)), rtxt, font(S(26)), C_INK2, anchor="rm")

    board_y = y4 + SEC4T

    for i, cell in enumerate(cells):
        r, c = divmod(i, cols)
        rn = min(cols, len(cells) - r * cols)            # 本行实际格数
        row_w = rn * CELL_W + (rn - 1) * STEP
        x = PAD + (RW - row_w) // 2 + c * (CELL_W + STEP)   # 每行各自居中
        y = board_y + r * (CELL_H + ROW_GAP)

        img.paste(fit_crop(imgs[i], CELL_W, CELL_IMG_H), (x, y))
        d.rectangle([x, y, x + CELL_W - 1, y + CELL_IMG_H - 1],
                    outline=C_FRAME, width=max(1, S(1)))

        # 画面角标：编号左上、时间码右上（白字深描边，任意明暗可读）
        draw_text(d, (x + S(14), y + S(12)), cell.get("num", "%02d" % (i + 1)),
                  font(S(30)), (255, 255, 255), stroke_width=max(1, S(3)), stroke_fill=C_NUM_STROKE)
        ts = cell.get("ts", "")
        if ts:
            draw_text(d, (x + CELL_W - S(14), y + S(16)), ts, font(S(22)), (255, 255, 255),
                      anchor="rt", stroke_width=max(1, S(3)), stroke_fill=C_NUM_STROKE)

        # 信息区
        iy = y + CELL_IMG_H
        d.line([(x, iy), (x + S(64), iy)], fill=C_ACCENT, width=max(1, S(4)))

        ht = " · ".join([v for v in (cell.get("num", ""), cell.get("scene", ""), cell.get("dur", "")) if v])
        draw_text(d, (x, iy + S(22)), ht, font(S(25)), C_INK)
        emo = cell.get("emotion", "")
        if emo:
            draw_text(d, (x + CELL_W, iy + S(22)), emo, font(S(24)), C_ACCENT, anchor="rt")

        ty = iy + S(62)
        for ln in wrap_cjk(d, cell.get("desc", ""), font(S(25)), CELL_W)[:2]:
            draw_text(d, (x, ty), ln, font(S(25)), C_INK2)
            ty += S(36)

        line = (cell.get("line") or "").strip()
        if line:
            draw_text(d, (x, ty + S(6)), "「%s」" % line, font(S(28), art=True), C_INK)
            ty += S(44)

        sub = " · ".join([v for v in (cell.get("sound", ""), cell.get("move", "")) if v])
        if sub:
            draw_text(d, (x, ty + S(6)), sub, font(S(20)), C_INK4)

    # ================= ⑤⑥ =================
    y56 = board_y + BOARD_H + GAP3
    d.line([(0, y56), (W, y56)], fill=C_DIV, width=max(1, S(1)))

    c5w = S(1120)
    section_head(PAD, y56 + S(16), "5", "光影与材质", "LIGHTING & MATERIAL")
    mats = data.get("materials") or []
    mx, mw, mh = PAD, S(260), S(170)
    for i, m in enumerate(mats[:4]):
        px = mx + i * (mw + S(20))
        pic = None
        if m.get("img") and os.path.exists(m["img"]):
            pic = load_asset(m["img"], m.get("crop"))
        elif m.get("cell"):
            idx = max(1, min(len(imgs), int(m["cell"]))) - 1
            src = imgs[idx]
            sw, sh = src.size
            cw2, ch2 = int(sw * 0.34), int(sh * 0.34)
            ox = int((sw - cw2) * float(m.get("ax", 0.5)))
            oy = int((sh - ch2) * float(m.get("ay", 0.5)))
            pic = src.crop((ox, oy, ox + cw2, oy + ch2))
        if pic is not None:
            img.paste(fit_crop(pic, mw, mh), (px, y56 + S(96)))
            d.rectangle([px, y56 + S(96), px + mw - 1, y56 + S(96) + mh - 1],
                        outline=C_FRAME, width=max(1, S(1)))
        else:
            d.rectangle([px, y56 + S(96), px + mw - 1, y56 + S(96) + mh - 1],
                        fill=C_BAND, outline=C_SEP, width=max(1, S(1)))
        draw_text(d, (px, y56 + S(96) + mh + S(14)), m.get("label", ""), font(S(23)), C_INK)
        draw_text(d, (px, y56 + S(96) + mh + S(46)), m.get("note", ""), font(S(20)), C_INK4)

    x6 = PAD + c5w + S(80)
    section_head(x6, y56 + S(16), "6", "摄影与技术说明", "CINEMATOGRAPHY")
    tech = data.get("tech") or []
    per_col = (len(tech) + 1) // 2
    for i, t in enumerate(tech[:10]):
        col, row = divmod(i, per_col if per_col else 1)
        px = x6 + col * S(520)
        py3 = y56 + S(100) + row * S(56)
        d.rectangle([px, py3 + S(6), px + S(14), py3 + S(20)], outline=C_ACCENT, width=max(1, S(2)))
        draw_text(d, (px + S(26), py3), t.get("k", ""), font(S(22)), C_INK4)
        draw_text(d, (px + S(26) + S(116), py3), t.get("v", ""), font(S(23)), C_INK2)

    # ================= 页脚 =================
    fy = H - FOOTER_H
    d.line([(0, fy), (W, fy)], fill=C_DIV, width=max(1, S(1)))
    draw_text(d, (PAD, fy + FOOTER_H // 2), "风格卡 %s" % data.get("style", ""),
              font(S(20)), C_INK4, anchor="lm")
    draw_text(d, (W - PAD, fy + FOOTER_H // 2),
              "%s · %d / %d" % (data.get("sb", ""), data.get("index", 1), data.get("total", 1)),
              font(S(20)), C_INK4, anchor="rm")

    img.save(out_path)
    return out_path


# ---------------- 模型版 · raw（给视频模型，零文字） ----------------
def build_raw(data, cells_dir, out_path, f, assets_dir=None):
    """模型版（给视频模型）：2–6 格网格，每格严格 16:9，零文字零页眉页脚。

    格数按段落实际关键帧数（与 table 版同一批 cells）：2–3 格单行、4 格 2×2、
    5–6 格 3×2。6 格时整张仍为 2352×1000；格数更少时高度不缩小，网格居中。

    用途：整张可作分镜参考；按格坐标裁开即对应张数的 16:9 单帧，
    可直接用作图生视频的首帧。格间纯色安全边，裁切不会带进邻格残边。
    """
    cells, imgs = load_cells(data, cells_dir)
    cols, rows = grid_of(len(cells))
    W = int(2352 * f)
    GAP = int(10 * f)

    gw = ((W - GAP * (cols + 1)) // cols) // 16 * 16
    gh = gw * 9 // 16
    grid_w = gw * cols + GAP * (cols + 1)
    grid_h = gh * rows + GAP * (rows + 1)
    # 6 格及以下单行版保持 2352×1000；2×2（4 格）时格宽翻倍，画布按网格长高，
    # 否则网格会溢出画布、顶格被裁掉半行。
    H = max(int(1000 * f), grid_h + GAP * 4)
    ox = (W - grid_w) // 2
    oy = (H - grid_h) // 2

    img = Image.new("RGB", (W, H), C_BG)

    for i, _cell in enumerate(cells):
        r, c = divmod(i, cols)
        x = ox + GAP + c * (gw + GAP)
        y = oy + GAP + r * (gh + GAP)
        img.paste(fit_crop(imgs[i], gw, gh), (x, y))

    img.save(out_path)
    return out_path


LAYOUTS = {
    "table": build_table,
    "raw": build_raw,
}


def main():
    global FONT_PATH, ART_PATH
    ap = argparse.ArgumentParser(description="按 SB-STYLE 版式规范合成故事板（S12-b），支持段落板/模型版两版式")
    ap.add_argument("--data", help="单张数据 JSON 路径")
    ap.add_argument("--cells", required=True, help="无字单格画面目录（含 P01-KF01.png 等）")
    ap.add_argument("--assets", default=None,
                    help="资产图目录（character-<id>*.png / prop-<id>*.png / scene-<id>*.png）；缺省则① ② 区降级为文字")
    ap.add_argument("--out", help="输出故事板路径（单张模式）")
    ap.add_argument("--batch", help="批量模式：数据 JSON 所在目录")
    ap.add_argument("--outdir", help="批量模式输出目录")
    ap.add_argument("--layout", choices=["table", "raw", "all"], default="all",
                    help="版式：table 段落板（给人看）/ raw 模型版（给视频模型，零文字）/ all 两版都出（默认 all）")
    ap.add_argument("--size", choices=["4k", "hd"], default="4k", help="缩放：4k=1.0，hd=0.5")
    ap.add_argument("--font", default=None, help="正文字体路径；默认自动查找系统中文字体")
    ap.add_argument("--art-font", default=None,
                    help="艺术字字体路径；按风格卡时代美学取向传入（见 style-palette.md §二）")
    ap.add_argument("--palette", default=None, help="风格色 JSON 路径（见 templates/style-palette.md）")
    args = ap.parse_args()

    if args.palette:
        load_palette(args.palette)
    global C_BG, C_BAND, C_INK, C_INK2, C_INK3, C_INK4, C_FRAME, C_DIV, C_SEP, C_NUM_STROKE, C_ACCENT
    C_BG, C_BAND = PALETTE["base"], PALETTE["band"]
    C_INK, C_INK2 = PALETTE["ink"], PALETTE["ink2"]
    C_INK3, C_INK4 = PALETTE["ink3"], PALETTE["ink4"]
    C_FRAME, C_DIV, C_SEP = PALETTE["rule"], PALETTE["rule"], PALETTE["sep"]
    C_NUM_STROKE = PALETTE["num-stroke"]
    C_ACCENT = PALETTE.get("accent", PALETTE["rule"])

    f = 1.0 if args.size == "4k" else 0.5
    FONT_PATH = args.font or find_font()
    ART_PATH = find_font(args.art_font, ART_FONT_CANDIDATES) or FONT_PATH
    if not FONT_PATH:
        print("WARNING: 未找到中文字体，将用 PIL 默认字体（中文可能显示为方块）", file=sys.stderr)
        FONT_PATH = ART_PATH = "C:/Windows/Fonts/simhei.ttf"

    def run_one(data, out_base):
        outs = []
        names = ["table", "raw"] if args.layout == "all" else [args.layout]
        for name in names:
            p = "%s-%s.png" % (out_base, name)
            outs.append(LAYOUTS[name](data, args.cells, p, f, args.assets))
        return outs

    if args.batch:
        outdir = args.outdir or args.batch
        os.makedirs(outdir, exist_ok=True)
        for fn in sorted(os.listdir(args.batch)):
            if not fn.endswith(".json"):
                continue
            with open(os.path.join(args.batch, fn), encoding="utf-8") as fh:
                data = json.load(fh)
            base = os.path.join(outdir, "storyboard-%s" % data.get("sb", fn[:-5]))
            for p in run_one(data, base):
                print("saved", p)
        return

    if not args.data or not args.out:
        ap.error("单张模式需要 --data 与 --out")
    with open(args.data, encoding="utf-8") as fh:
        data = json.load(fh)
    base = args.out.rsplit(".", 1)[0]
    for p in run_one(data, base):
        print("saved", p)


if __name__ == "__main__":
    main()
