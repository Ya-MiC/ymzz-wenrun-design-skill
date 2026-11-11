#!/usr/bin/env python3
"""Build derived 雲箋 PPTX, DOCX, and XLSX samples.

These files follow references/office-derivations.md. They are not original
masters. The v7.1 archive never names these formats.
"""

from __future__ import annotations

import re
import zipfile
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn as ppt_qn
from pptx.util import Emu as PptEmu
from pptx.util import Inches, Pt as PptPt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "samples"

INK = "3D3833"
INK2 = "6E675E"
PAPER = "F8F6EF"
SKY = "B9DDF1"
PINK = "F4DDE7"
VIOLET = "CDBFE0"
CARD = "FCFCF9"
LINE = "E9E7E0"
FACE = "Noto Sans SC"

SCHEME = {
    "dk1": INK,
    "lt1": PAPER,
    "dk2": INK2,
    "lt2": CARD,
    "accent1": SKY,
    "accent2": PINK,
    "accent3": VIOLET,
    "accent4": SKY,
    "accent5": PINK,
    "accent6": VIOLET,
    "hlink": INK,
    "folHlink": INK,
}

ALLOWED = {
    INK, INK2, "9C948A", PAPER, SKY, PINK, VIOLET, CARD, "FEFDFC", "FFFFFE", LINE,
}


def rgb(value: str) -> RGBColor:
    return RGBColor.from_string(value)


def ppt_rgb(value: str) -> PptRGB:
    return PptRGB.from_string(value)


def set_run_font(run, size_pt: float, color: str, bold: bool = False) -> None:
    run.font.name = FACE
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)
    run.font.italic = False
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(attr), FACE)


def shade_cell(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    for old in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_border(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        element = borders.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def paragraph_format(paragraph, after_pt: float = 8, before_pt: float = 0, keep_next: bool = False) -> None:
    fmt = paragraph.paragraph_format
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fmt.line_spacing = 1.7
    fmt.space_after = Pt(after_pt)
    fmt.space_before = Pt(before_pt)
    fmt.keep_together = True
    fmt.keep_with_next = keep_next


def add_text(paragraph, text: str, size: float, color: str = INK, bold: bool = False) -> None:
    run = paragraph.add_run(text)
    set_run_font(run, size, color, bold)


def paint_slide(slide, color: str) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = ppt_rgb(color)


def add_textbox(slide, left, top, width, height, text, size, color=INK, bold=False):
    shape = slide.shapes.add_textbox(left, top, width, height)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.auto_size = None
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    paragraph = frame.paragraphs[0]
    paragraph.alignment = PP_ALIGN.LEFT
    run = paragraph.add_run()
    run.text = text
    run.font.name = FACE
    run.font.size = PptPt(size)
    run.font.bold = bold
    run.font.color.rgb = ppt_rgb(color)
    run.font.italic = False
    r_pr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        node = r_pr.find(ppt_qn(tag))
        if node is None:
            node = r_pr.makeelement(ppt_qn(tag), {})
            r_pr.append(node)
        node.set("typeface", FACE)
    return shape


def add_chip(slide, left, top, width, height, fill: str) -> None:
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = ppt_rgb(fill)
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def build_pptx(path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = "晏銘湛箴溫潤技能樣本"
    prs.core_properties.subject = "Derived 雲箋 sample from the wenrun skill. Not an original master."
    prs.core_properties.category = "ymzz wenrun"
    blank = prs.slide_layouts[6]
    margin = Inches(0.5)

    slide = prs.slides.add_slide(blank)
    paint_slide(slide, PAPER)
    add_chip(slide, margin, Inches(0.72), Inches(1.15), Inches(0.38), SKY)
    add_textbox(slide, margin, Inches(0.76), Inches(1.15), Inches(0.32), "雲箋", 12, INK)
    add_textbox(slide, margin, Inches(1.7), Inches(10.5), Inches(1.3), "同一套溫潤", 21, INK)
    add_textbox(
        slide,
        margin,
        Inches(3.15),
        Inches(9.2),
        Inches(1.6),
        "簡報、文件、試算表，和畫面上的介面，用同一套色、同一套字級。",
        10.5,
        INK,
    )
    add_textbox(slide, margin, Inches(6.5), Inches(8), Inches(0.4), "晏銘湛箴", 9, INK2)

    slide = prs.slides.add_slide(blank)
    paint_slide(slide, PAPER)
    add_textbox(slide, margin, Inches(0.5), Inches(10), Inches(0.7), "四色封頂", 21, INK)
    add_textbox(
        slide,
        margin,
        Inches(1.35),
        Inches(11),
        Inches(0.8),
        "雲箋只有這四色。正文用墨色，不用淺天空藍當字。",
        10.5,
        INK,
    )
    chips = [("暖紙白", PAPER, True), ("淺天空藍", SKY, False), ("荷花粉", PINK, False), ("淡紫", VIOLET, False)]
    for index, (name, color, keyed) in enumerate(chips):
        left = Inches(0.5 + index * 3.1)
        add_chip(slide, left, Inches(2.6), Inches(2.4), Inches(1.35), color)
        if keyed:
            key = slide.shapes.add_shape(1, left, Inches(2.6), Inches(2.4), Inches(1.35))
            key.fill.background()
            key.line.color.rgb = ppt_rgb(INK2)
            key.line.width = PptEmu(12700)
            key.shadow.inherit = False
        add_textbox(slide, left, Inches(4.15), Inches(2.4), Inches(0.7), name, 10.5, INK)
    add_textbox(slide, margin, Inches(6.4), Inches(11), Inches(0.5), "暖紙白和紙面同色，所以外圍用次墨畫了識別線。線不是色值。", 9, INK2)

    slide = prs.slides.add_slide(blank)
    paint_slide(slide, PAPER)
    add_textbox(slide, margin, Inches(0.5), Inches(11), Inches(0.7), "先讀色，再做畫面", 21, INK)
    lines = [
        "一個畫面只用一套。雲箋和陶土不要混在同一張表。",
        "載入、空、錯誤，都用同一套墨色和同一套句子。",
        "投影片放不下就加一頁。不要把字縮到看不見。",
    ]
    top = 1.6
    for line in lines:
        add_chip(slide, margin, Inches(top), Inches(0.18), Inches(0.38), PINK)
        add_textbox(slide, Inches(0.9), Inches(top), Inches(11), Inches(0.7), line, 10.5, INK)
        top += 1.15
    add_textbox(slide, margin, Inches(6.45), Inches(11.5), Inches(0.5), "這三頁是推導樣本，不是原始母片。深藤紫沒有用在這裡。", 9, INK2)
    prs.save(path)


def build_docx(path: Path) -> None:
    doc = Document()
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.header_distance = Inches(0.3)
        section.footer_distance = Inches(0.3)
    background = OxmlElement("w:background")
    background.set(qn("w:color"), PAPER)
    doc.element.insert(0, background)
    doc.settings.element.append(OxmlElement("w:displayBackgroundShape"))

    normal = doc.styles["Normal"]
    normal.font.name = FACE
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = rgb(INK)
    r_pr = normal.element.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(attr), FACE)

    title = doc.add_paragraph()
    paragraph_format(title, after_pt=6, keep_next=True)
    add_text(title, "同一套溫潤", 21, INK)

    body = doc.add_paragraph()
    paragraph_format(body, after_pt=8)
    add_text(body, "這份文件用雲箋。標題和內文都是墨色。淺天空藍只做標籤，不做段落的字色。", 10.5, INK)

    note = doc.add_paragraph()
    paragraph_format(note, after_pt=10, keep_next=True)
    add_text(note, "八個鎖定色裡，這份樣本只用雲箋那四色。陶土留在色卡，不混進這張表。", 10.5, INK)

    table = doc.add_table(rows=1, cols=3)
    table.autofit = True
    headers = ("名稱", "角色", "怎麼用")
    for index, label in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = ""
        paragraph = cell.paragraphs[0]
        paragraph_format(paragraph, after_pt=2, keep_next=True)
        add_text(paragraph, label, 10.5, INK)
        shade_cell(cell, SKY)
        set_cell_border(cell, LINE)
    rows = [
        ("暖紙白", "紙面", "整頁的底"),
        ("淺天空藍", "資訊", "表頭和小標籤"),
        ("荷花粉", "強調", "提醒，不用來寫正文"),
        ("淡紫", "裝飾", "光暈和點綴"),
    ]
    for name, role, use in rows:
        cells = table.add_row().cells
        for index, value in enumerate((name, role, use)):
            cells[index].text = ""
            paragraph = cells[index].paragraphs[0]
            paragraph_format(paragraph, after_pt=2)
            add_text(paragraph, value, 10.5, INK)
            shade_cell(cells[index], CARD)
            set_cell_border(cells[index], LINE)

    closing = doc.add_paragraph()
    paragraph_format(closing, before_pt=12, after_pt=4)
    add_text(closing, "字型指定為 Noto Sans SC。若這台電腦沒有這套字，閱讀程式會換成別的字，那不是另一個指定字型。", 9, INK2)

    gap = doc.add_paragraph()
    paragraph_format(gap, after_pt=0)
    add_text(gap, "深藤紫仍是提案，這份文件沒有用它。這是推導樣本，不是原始母片。", 9, INK2)
    doc.core_properties.title = "晏銘湛箴溫潤技能樣本"
    doc.core_properties.subject = "Derived 雲箋 sample. Not an original master."
    doc.save(path)


def build_xlsx(path: Path) -> None:
    book = Workbook()
    sheet = book.active
    sheet.title = "雲箋"
    headers = ("名稱", "角色", "怎麼用")
    rows = [
        ("暖紙白", "紙面", "整頁的底"),
        ("淺天空藍", "資訊", "表頭和小標籤"),
        ("荷花粉", "強調", "提醒，不用來寫正文"),
        ("淡紫", "裝飾", "光暈和點綴"),
    ]
    header_font = Font(name=FACE, size=10.5, color=INK, bold=False)
    body_font = Font(name=FACE, size=10.5, color=INK, bold=False)
    quiet_font = Font(name=FACE, size=9, color=INK2, bold=False)
    header_fill = PatternFill("solid", fgColor=SKY)
    card_fill = PatternFill("solid", fgColor=CARD)
    wrap = Alignment(wrap_text=True, vertical="center", horizontal="left")
    for col, label in enumerate(headers, 1):
        cell = sheet.cell(1, col, label)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = wrap
    for row_index, values in enumerate(rows, 2):
        for col, value in enumerate(values, 1):
            cell = sheet.cell(row_index, col, value)
            cell.font = body_font
            cell.fill = card_fill
            cell.alignment = wrap
        sheet.row_dimensions[row_index].height = 22
    sheet.row_dimensions[1].height = 22
    widths = (16, 14, 28)
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.freeze_panes = "A2"
    sheet.print_title_rows = "1:1"
    sheet.page_setup.fitToPage = True
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.page_setup.orientation = "landscape"
    sheet.page_margins = PageMargins(left=0.5, right=0.5, top=0.5, bottom=0.5, header=0.2, footer=0.2)
    sheet.sheet_view.showGridLines = False
    sheet.oddHeader.left.text = ""

    steps = book.create_sheet("間距")
    steps["A1"] = "名稱"
    steps["B1"] = "像素"
    steps["C1"] = "推導點數"
    for col in range(1, 4):
        cell = steps.cell(1, col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(vertical="center", horizontal="left" if col == 1 else "right")
    spacing = (("正文", 14, 10.5), ("標題", 28, 21), ("小標", 20, 15), ("邊距", 48, 36))
    for index, (name, px, pt) in enumerate(spacing, 2):
        steps.cell(index, 1, name).font = body_font
        px_cell = steps.cell(index, 2, px)
        px_cell.font = body_font
        px_cell.alignment = Alignment(horizontal="right")
        px_cell.number_format = "0"
        pt_cell = steps.cell(index, 3, pt)
        pt_cell.font = body_font
        pt_cell.alignment = Alignment(horizontal="right")
        pt_cell.number_format = "0.00"
        for col in range(1, 4):
            steps.cell(index, col).fill = card_fill
    steps["A7"] = "點數由 1 像素 = 0.75 點換算。這是推導，不是原始 token。"
    steps["A7"].font = quiet_font
    steps.merge_cells("A7:C7")
    for index, width in enumerate((16, 12, 14), 1):
        steps.column_dimensions[get_column_letter(index)].width = width
    steps.freeze_panes = "A2"
    steps.print_title_rows = "1:1"
    steps.page_setup.fitToPage = True
    steps.page_setup.fitToWidth = 1
    steps.page_setup.fitToHeight = 0
    steps.page_margins = PageMargins(left=0.5, right=0.5, top=0.5, bottom=0.5, header=0.2, footer=0.2)
    steps.sheet_view.showGridLines = False
    book.properties.title = "晏銘湛箴溫潤技能樣本"
    book.properties.subject = "Derived 雲箋 sample. Not an original master."
    book.save(path)


THEME_VAL = {
    "accent1": SKY,
    "accent2": PINK,
    "accent3": VIOLET,
    "accent4": SKY,
    "accent5": PINK,
    "accent6": VIOLET,
    "dk1": INK,
    "lt1": PAPER,
    "dk2": INK2,
    "lt2": CARD,
    "dark1": INK,
    "light1": PAPER,
    "dark2": INK2,
    "light2": CARD,
    "text1": INK,
    "background1": PAPER,
    "text2": INK2,
    "background2": CARD,
    "hyperlink": INK,
    "followedHyperlink": INK,
}


def retint_cached_theme(xml: str) -> str:
    """Word stores a hex hint beside each theme slot. Point the hint at 雲箋."""

    def one_tag(match: re.Match) -> str:
        tag = match.group(0)
        theme = re.search(r'w:theme(?:Color|Fill)="([^"]+)"', tag)
        color = THEME_VAL.get(theme.group(1) if theme else "")
        if not color:
            return tag
        tag = re.sub(r'(w:(?:val|color|fill)=")[0-9A-Fa-f]{6}(")', rf"\g<1>{color}\g<2>", tag)
        return tag

    return re.sub(r"<w:[^>]*w:theme(?:Color|Fill)=\"[^\"]+\"[^>]*>", one_tag, xml)


def patch_theme(xml: str) -> str:
    def scheme_child(match: re.Match) -> str:
        name = match.group(1)
        color = SCHEME[name]
        return f'<a:{name}><a:srgbClr val="{color}"/></a:{name}>'

    xml = re.sub(r"<a:(dk1|lt1|dk2|lt2|accent[1-6]|hlink|folHlink)>.*?</a:\1>", scheme_child, xml, flags=re.DOTALL)
    xml = re.sub(r'(<a:(?:latin|ea|cs)[^>]*typeface=")[^"]*(")', rf"\1{FACE}\2", xml)
    xml = re.sub(r'(<a:font script="[^"]+" typeface=")[^"]*(")', rf"\1{FACE}\2", xml)
    xml = xml.replace('typeface=""', f'typeface="{FACE}"')
    # Office's default effect shadow is cold black. The grammar uses warm ink.
    xml = xml.replace('<a:srgbClr val="000000">', f'<a:srgbClr val="{INK}">')
    return xml


def patch_package(path: Path) -> None:
    blob = path.read_bytes()
    source = zipfile.ZipFile(BytesIO(blob))
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as target:
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename.endswith(".xml"):
                text = data.decode("utf-8")
                if "clrScheme" in text:
                    text = patch_theme(text)
                text = retint_cached_theme(text)
                data = text.encode("utf-8")
            target.writestr(info, data)
    path.write_bytes(buffer.getvalue())


def unexpected_colors(path: Path) -> list[str]:
    found = set()
    with zipfile.ZipFile(path) as package:
        for name in package.namelist():
            if not name.endswith((".xml", ".rels")):
                continue
            text = package.read(name).decode("utf-8", "ignore")
            found.update(item.upper() for item in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', text))
            found.update(item.upper() for item in re.findall(r'w:fill="([0-9A-Fa-f]{6})"', text))
            found.update(item.upper() for item in re.findall(r'w:color="([0-9A-Fa-f]{6})"', text))
            found.update(item.upper() for item in re.findall(r'rgb="(?:FF)?([0-9A-Fa-f]{6})"', text))
            found.update(item.upper() for item in re.findall(r'lastClr="([0-9A-Fa-f]{6})"', text))
    return sorted(found - ALLOWED)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        OUT / "yunjian-brief.pptx": build_pptx,
        OUT / "yunjian-brief.docx": build_docx,
        OUT / "yunjian-brief.xlsx": build_xlsx,
    }
    for path, builder in files.items():
        builder(path)
        patch_package(path)
        extra = unexpected_colors(path)
        if extra:
            raise SystemExit(f"{path.name} has colors outside the 雲箋 sample: {extra}")
        print(path.name)


if __name__ == "__main__":
    main()
