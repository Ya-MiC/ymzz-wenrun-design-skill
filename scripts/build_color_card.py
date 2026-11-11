#!/usr/bin/env python3
"""Build a readable color card from the v7.1 hex values.

The card is a reading aid. It does not invent colors and it does not
replace the whitepaper swatch pages. Sticker, cover, and emblem colors
are intentionally absent.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_PNG = ROOT / "assets" / "color-card.png"
OUT_SVG = ROOT / "assets" / "color-card.svg"
OUT_LAYOUT = ROOT / "assets" / "color-card.layout.json"

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
INK = "#3D3833"
INK_2 = "#6E675E"
PAPER = "#F8F6EF"
DUSK_PAPER = "#E6E1D5"
WARM_BLACK = "#1F1B16"

W = 1240
PAD = 64
GAP = 22
SW = 252
SH = 108
RADIUS = 12


def rel_lum(hex_color: str) -> float:
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = rgb(hex_color)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def text_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        trial = current + ch
        if current and text_width(draw, trial, face) > max_w:
            lines.append(current)
            current = ch
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


CLOUD = [
    ("暖紙白", "#F8F6EF", "底層表面、大面積留白"),
    ("淺天空藍", "#B9DDF1", "標籤、手繪裝飾、資訊類提示"),
    ("荷花粉", "#F4DDE7", "輕柔點綴、重點提示、情感類反饋"),
    ("淡紫", "#CDBFE0", "過渡色、聚焦光暈、次級裝飾"),
]
EARTH = [
    ("燕麥米", "#E8E3CC", "淺表面、卡片"),
    ("鼠尾草綠", "#B7C8A8", "成功態、自然語義、標籤"),
    ("亞麻金", "#CBBF9E", "高亮、進度、溫和警示"),
    ("可可棕", "#A38E7A", "深點綴、邊飾。墨色在其上 3.70，不夠正文"),
]
DUSK = [
    ("暮紙白", "#E6E1D5", "深色模式主文字"),
    ("霧靄藍", "#7C9DB5", "資訊標籤、手繪裝飾"),
    ("乾藕粉", "#B394A3", "重點提示、情感反饋"),
    ("菸灰紫", "#93879F", "聚焦光暈、次級裝飾"),
]
WOOD = [
    ("夜麥米", "#D9D3C0", "深色模式主文字"),
    ("苔蘚綠", "#7E8E6F", "成功態、自然語義"),
    ("褐亞麻", "#9E9073", "高亮、進度"),
    ("深可可", "#7C6B59", "只作填充、邊界、裝飾，不作文字"),
]
PROPOSALS = [
    ("可可文字級", "#9D8A76", "派生·已驗證。只作暮林文字，不是新色相"),
    ("深藤紫", "#75589D", "提案·待確認。沒有鎖定，不能當已批准的品牌色"),
]
INKS = [
    ("ink-1 正文墨", "#3D3833", "淺色正文"),
    ("ink-2 次級", "#6E675E", "次級文字"),
    ("ink-3 佔位", "#9C948A", "只作佔位與禁用，2.77，不能閱讀"),
]
DARK_BG = [
    ("bg-0 暖黑", "#1F1B16", "深色最底，不是純黑"),
    ("bg-1", "#2A241D", "卡片"),
    ("bg-2", "#352E25", "浮起表面"),
    ("bg-3", "#423A2F", "浮層"),
]
DARK_INK = [
    ("深色 ink-1", "#E6E1D5", "與暮紙白同一色值"),
    ("深色 ink-2", "#B3AC9F", "深色次級文字"),
    ("深色 ink-3", "#7A7268", "深色佔位與禁用"),
]

STATUS_DARK = (
    "深色衍生的狀態標籤互相矛盾，此處全部保留，不升成最終鎖定："
    "docs/01 為衍生·待驗證；tokens.css 為鎖定·已驗證；"
    "白皮書為計算已驗證、待三引擎真機複測；"
    "根目錄契約 SKILL 為計算已驗證·待終鎖。"
)
STATUS_NEUTRAL = (
    "中性層不佔四色名額。狀態同樣並存："
    "docs/01 為提案·待確認；tokens.css 為鎖定·已確認。"
)


def build() -> dict:
    probe = Image.new("RGB", (W, 400), rgb(PAPER))
    draw = ImageDraw.Draw(probe)
    f_title = font(40)
    f_sub = font(18)
    f_sec = font(22)
    f_status = font(15)
    f_name = font(18)
    f_hex = font(16)
    f_role = font(14)
    f_foot = font(15)

    content_w = W - PAD * 2
    y = PAD
    texts: list[dict] = []
    swatches: list[dict] = []
    bands: list[dict] = []

    def add_text(s: str, face, fill: str, x: int, max_w: int, gap: int = 8) -> None:
        nonlocal y
        for line in wrap(draw, s, face, max_w):
            width = text_width(draw, line, face)
            if width > max_w:
                raise SystemExit(f"line exceeds column: {line}")
            bbox = draw.textbbox((x, y), line, font=face)
            texts.append({"text": line, "x": x, "y": y, "fill": fill, "size": face.size, "bbox": bbox})
            y = bbox[3] + gap

    def section_title(title: str, note: str | None = None) -> None:
        nonlocal y
        y += 8
        add_text(title, f_sec, INK, PAD, content_w, 6)
        if note:
            add_text(note, f_status, INK_2, PAD, content_w, 10)
        else:
            y += 6

    def swatch_row(items: list[tuple[str, str, str]], label_fill: str, on_dark: bool) -> None:
        nonlocal y
        if on_dark:
            y += 24
        row_top = y
        row_texts: list[dict] = []
        row_swatches: list[dict] = []
        bottom = y + SH
        for i, (name, hx, role) in enumerate(items):
            x = PAD + i * (SW + GAP)
            if x + SW > W - PAD:
                raise SystemExit(f"swatch overflows: {name}")
            row_swatches.append({"name": name, "hex": hx.upper(), "x": x, "y": y, "w": SW, "h": SH})
            ly = y + SH + 12
            for line, face, step in (
                (name, f_name, 6),
                (hx.upper(), f_hex, 4),
            ):
                width = text_width(draw, line, face)
                if width > SW:
                    raise SystemExit(f"label overflows swatch: {line}")
                bbox = draw.textbbox((x, ly), line, font=face)
                row_texts.append({"text": line, "x": x, "y": ly, "fill": label_fill, "size": face.size, "bbox": bbox})
                ly = bbox[3] + step
            for line in wrap(draw, role, f_role, SW):
                bbox = draw.textbbox((x, ly), line, font=f_role)
                row_texts.append({"text": line, "x": x, "y": ly, "fill": label_fill, "size": f_role.size, "bbox": bbox})
                ly = bbox[3] + 2
            bottom = max(bottom, ly)
        if on_dark:
            bands.append({"x": 0, "y": row_top - 16, "w": W, "h": (bottom - (row_top - 16)) + 20, "fill": WARM_BLACK})
        swatches.extend(row_swatches)
        texts.extend(row_texts)
        y = bottom + (36 if on_dark else 20)

    add_text("晏銘湛箴", f_title, INK, PAD, content_w, 6)
    add_text("溫潤色卡", f_title, INK, PAD, content_w, 10)
    add_text("八個鎖定色。機器色值來源是 tokens.css。此圖只彙總，不新設計。", f_sub, INK_2, PAD, content_w, 4)
    add_text("陶土是淺色系，不是深色模式。深藤紫仍是提案。", f_sub, INK_2, PAD, content_w, 18)

    section_title("雲箋　【鎖定】　每套四色封頂　·　淺色")
    swatch_row(CLOUD, INK, False)

    section_title("陶土　【鎖定】　每套四色封頂　·　淺色大地暖調，不是深色")
    add_text("tokens.css 把鼠尾草綠寫成 #b7c8a8。與文件、白皮書的 #B7C8A8 是同一個 sRGB。", f_status, INK_2, PAD, content_w, 10)
    swatch_row(EARTH, INK, False)

    section_title("暮靄　雲箋的莫蘭迪深版", STATUS_DARK)
    swatch_row(DUSK, DUSK_PAPER, True)

    section_title("暮林　陶土的莫蘭迪深版", STATUS_DARK)
    swatch_row(WOOD, DUSK_PAPER, True)

    section_title("不佔四色名額　·　派生與提案", "這兩色不是第九個品牌色，也不進四色封頂。深藤紫未經確認。")
    swatch_row(PROPOSALS, INK, False)

    section_title("中性結構層", STATUS_NEUTRAL)
    swatch_row(INKS, INK, False)
    swatch_row(DARK_BG, INK, False)
    swatch_row(DARK_INK, INK, False)

    y += 8
    for line in (
        "同一畫面只用一套。正文用墨色，原色不作正文。可可棕底不夠正文對比。",
        "對所在底色對比低於 1.2 的色塊，外圍用 ink-2 畫識別線。線不是色值。",
        "不把貼紙色、封面排版色、徽章色算進這張產品色卡。",
        "原色卡見白皮書第 3 頁雲箋、第 5 頁深藤紫提案、第 6 頁陶土、第 7 頁暮靄與暮林。",
    ):
        add_text(line, f_foot, INK, PAD, content_w, 6)

    height = y + PAD
    image = Image.new("RGB", (W, height), rgb(PAPER))
    canvas = ImageDraw.Draw(image)
    for band in bands:
        canvas.rectangle((band["x"], band["y"], band["x"] + band["w"], band["y"] + band["h"]), fill=rgb(band["fill"]))
    for sw in swatches:
        backdrop = WARM_BLACK if any(
            b["y"] <= sw["y"] <= b["y"] + b["h"] for b in bands
        ) else PAPER
        outline = rgb(INK_2) if contrast(sw["hex"], backdrop) < 1.2 else None
        sw["keyline"] = INK_2 if outline else None
        canvas.rounded_rectangle(
            (sw["x"], sw["y"], sw["x"] + sw["w"], sw["y"] + sw["h"]),
            radius=RADIUS,
            fill=rgb(sw["hex"]),
            outline=outline,
            width=3 if outline else 0,
        )
    for item in texts:
        canvas.text((item["x"], item["y"]), item["text"], font=font(item["size"]), fill=rgb(item["fill"]))

    # Legibility checks against the pixels and the measured boxes.
    for item in texts:
        x0, y0, x1, y1 = item["bbox"]
        if x0 < 32 or y0 < 32 or x1 > W - 32 or y1 > height - 32:
            raise SystemExit(f"text clipped: {item['text']} {item['bbox']} canvas {W}x{height}")
    for sw in swatches:
        if sw["y"] < 32 or sw["y"] + sw["h"] > height - 32 or sw["x"] < 32 or sw["x"] + sw["w"] > W - 32:
            raise SystemExit(f"swatch clipped: {sw}")
        cx = sw["x"] + sw["w"] // 2
        cy = sw["y"] + sw["h"] // 2
        if image.getpixel((cx, cy)) != rgb(sw["hex"]):
            raise SystemExit(f"center pixel mismatch for {sw['name']}: {image.getpixel((cx, cy))}")
        # Corners of a rounded swatch stay inside the fill at this radius.
        inset = RADIUS + 2
        for px, py in (
            (sw["x"] + inset, sw["y"] + inset),
            (sw["x"] + sw["w"] - inset - 1, sw["y"] + sw["h"] - inset - 1),
        ):
            if image.getpixel((px, py)) != rgb(sw["hex"]):
                raise SystemExit(f"inset pixel mismatch for {sw['name']} at {(px, py)}")

    def inside_band(box) -> bool:
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        return any(b["x"] <= cx <= b["x"] + b["w"] and b["y"] <= cy <= b["y"] + b["h"] for b in bands)

    for item in texts:
        on_band = inside_band(item["bbox"])
        if item["fill"] == DUSK_PAPER and not on_band:
            raise SystemExit(f"light label left the dark band: {item['text']}")
        if item["fill"] in {INK, INK_2} and on_band:
            raise SystemExit(f"ink label fell onto the dark band: {item['text']}")

    text_boxes = [tuple(item["bbox"]) for item in texts]
    for i, a in enumerate(text_boxes):
        for b in text_boxes[i + 1 :]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                raise SystemExit(f"text overlap {a} {b}")

    image.save(OUT_PNG, "PNG", optimize=True)
    write_svg(texts, swatches, bands, height)
    layout = {
        "width": W,
        "height": height,
        "background": PAPER,
        "swatches": swatches,
        "note": "Assembled reading card. Hex values are the v7.1 palette. Geometry is not a new design.",
    }
    OUT_LAYOUT.write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PNG} {W}x{height}")
    return layout


def xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_svg(texts: list[dict], swatches: list[dict], bands: list[dict], height: int) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img">',
        "<title>晏銘湛箴溫潤色卡</title>",
        "<desc>Locked 雲箋 and 陶土 colors, dark derivatives, neutrals, and the unconfirmed 深藤紫 proposal. Hex values come from wenrun-design-system v7.1 tokens.css. Sticker, cover, and emblem colors are not included.</desc>",
        f'<rect width="{W}" height="{height}" fill="{PAPER}"/>',
    ]
    for band in bands:
        parts.append(
            f'<rect x="{band["x"]}" y="{band["y"]}" width="{band["w"]}" height="{band["h"]}" fill="{band["fill"]}"/>'
        )
    for sw in swatches:
        stroke = f' stroke="{INK_2}" stroke-width="3"' if sw.get("keyline") else ""
        parts.append(
            f'<rect x="{sw["x"]}" y="{sw["y"]}" width="{sw["w"]}" height="{sw["h"]}" rx="{RADIUS}" fill="{sw["hex"]}"{stroke}/>'
        )
    family = "Noto Sans SC Variable, Noto Sans SC, WenQuanYi Micro Hei, sans-serif"
    for item in texts:
        # SVG y is the baseline. PIL y is the top. Use the bbox top plus ascent approximation:
        # dominant-baseline hanging matches a top-origin well enough for the vector copy.
        parts.append(
            f'<text x="{item["x"]}" y="{item["y"]}" fill="{item["fill"]}" font-size="{item["size"]}" '
            f'font-family="{family}" dominant-baseline="hanging">{xml(item["text"])}</text>'
        )
    parts.append("</svg>")
    OUT_SVG.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
