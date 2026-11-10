#!/usr/bin/env python3
"""Check the wenrun skill package against the v7.1 sources.

The arithmetic in this file is a check. It does not replace tokens.css,
contrast-matrix.md, or the whitepaper, and it does not pick a winner
when those sources disagree.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

HASHES = {
    "assets/tokens/tokens.css": "217ca41de8a15fc612b17ec33b428470ffa155bedb8ddec73a47dba67aa85ad4",
    "assets/tokens/contrast-matrix.md": "6c1b0ae90ce775df505f5dfb02db35668f4a5fb3f6fbb7ce9d0232f39a8857af",
    "assets/tokens/motion.js": "9500b9a93999307f751e823c9c1e1634b4c6939c20b6c3bb11cc930aa1f1fd56",
    "assets/non-product/vibe-content.css": "feca22ca71018eabbcffdf859ac75fc3490320920a05fef8e052d37a4ba69141",
    "assets/original/color-whitepaper-v5.pdf": "6b0a4eb9ff753cc10381dafc0de564267687d36dc26c11c9d2e248afa52ab12e",
    "references/source/01-色彩系統-四套.md": None,
    "references/source/02-表面與字體.md": None,
    "references/source/11-審美憲章.md": None,
    "references/source/prompts-00-主提示詞.md": None,
    "references/source/prompts-01-色彩提示詞.md": None,
}

LOCKED = {
    "暖紙白": "F8F6EF",
    "淺天空藍": "B9DDF1",
    "荷花粉": "F4DDE7",
    "淡紫": "CDBFE0",
    "燕麥米": "E8E3CC",
    "鼠尾草綠": "B7C8A8",
    "亞麻金": "CBBF9E",
    "可可棕": "A38E7A",
}

# Transcribed from 色卡白皮書 v5, table 6-4. Not computed.
PDF_WOOD = {
    "D9D3C0": (Decimal("11.44"), Decimal("10.25"), Decimal("8.94")),
    "7E8E6F": (Decimal("4.88"), Decimal("4.37"), Decimal("3.82")),
    "9E9073": (Decimal("5.45"), Decimal("4.89"), Decimal("4.26")),
    "7C6B59": (Decimal("3.35"), Decimal("3.00"), Decimal("2.62")),
    "9D8A76": (Decimal("5.16"), Decimal("4.63"), Decimal("4.04")),
}

DARK_BG = ("1F1B16", "2A241D", "352E25")
FORBIDDEN_CARD = {
    "E8443A", "F5B301", "2B50C8", "111111", "ECE9E2", "92761F", "A3848F",
    "0A0C14", "FFCF6E", "FF5D7A", "7FB3FF", "FAF9F6", "F3F1EC", "5C467C",
    "614983", "664D89", "6B5190", "705496", "F5F5F4", "151513", "7E7C74",
    "4E4732",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel_lum(hex_color: str) -> float:
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str) -> Decimal:
    hi, lo = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    raw = (hi + 0.05) / (lo + 0.05)
    return Decimal(format(raw, ".10f")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def band(value: Decimal) -> str:
    if value >= Decimal("4.50"):
        return "body"
    if value >= Decimal("3.00"):
        return "large-or-boundary"
    return "decoration"


def parse_css_colors(text: str) -> list[tuple[str, str]]:
    return [
        (name, hx.upper())
        for name, hx in re.findall(r"(--[\w-]+)\s*:\s*#([0-9A-Fa-f]{6})\b", text)
    ]


def parse_matrix_wood(text: str) -> dict[str, tuple[Decimal, Decimal, Decimal]]:
    rows = {}
    for line in text.splitlines():
        if not line.startswith("|") or "--c-wood-" not in line:
            continue
        match = re.search(
            r"#([0-9A-Fa-f]{6}).*?\|\s*([0-9.*]+)\s*\|\s*([0-9.*]+)\s*\|\s*([0-9.*]+)\s*\|",
            line,
        )
        if not match:
            raise SystemExit(f"could not parse matrix row: {line}")
        hx, a, b, c = match.groups()
        rows[hx.upper()] = tuple(Decimal(part.replace("*", "")) for part in (a, b, c))
    return rows


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit("SKILL.md is missing YAML frontmatter")
    raw = match.group(1)
    data: dict[str, str] = {}
    current = None
    buf: list[str] = []
    fold = None
    for line in raw.splitlines():
        if current and (line.startswith("  ") or line.startswith("\t")):
            buf.append(line.strip())
            continue
        if current is not None:
            data[current] = fold_value(fold, buf)
            current = None
            buf = []
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value in {">-", ">", "|"}:
            current = key.strip()
            fold = value
            buf = []
        else:
            data[key.strip()] = value.strip().strip("'\"")
    if current is not None:
        data[current] = fold_value(fold, buf)
    return data


def fold_value(style: str | None, lines: list[str]) -> str:
    if style == ">":
        return " ".join(lines)
    if style == ">-":
        return " ".join(lines).rstrip()
    return "\n".join(lines)


def markdown_links(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0].strip()
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)} -> missing {target}")
    return errors


def contrast_report(matrix: dict[str, tuple[Decimal, Decimal, Decimal]]) -> str:
    lines = [
        "# Contrast check",
        "",
        "This file is arithmetic from this package. It is not `scripts/color_math.py` and not `scripts/contrast_verify.py`. Those files are named in the whitepaper and in `contrast-matrix.md`, and they were not in the v7.1 archive.",
        "",
        "Method: WCAG 2.1 relative luminance, rounded half up to two decimals. The result is a check. It does not replace either published table and it does not choose a winner.",
        "",
        "## 暮林 bg-0 / bg-1 / bg-2",
        "",
        "Backgrounds are `#1F1B16`, `#2A241D`, `#352E25`.",
        "",
        "| Hex | Stop | contrast-matrix.md | whitepaper table 6-4 | recomputed here | bands |",
        "|---|---|---|---|---|---|",
    ]
    names = ("bg-0", "bg-1", "bg-2")
    for hx, pdf_row in PDF_WOOD.items():
        matrix_row = matrix[hx]
        for index, bg in enumerate(DARK_BG):
            recomputed = contrast(hx, bg)
            bands = {band(matrix_row[index]), band(pdf_row[index]), band(recomputed)}
            band_text = bands.pop() if len(bands) == 1 else "DIFFER"
            lines.append(
                f"| `{hx}` | {names[index]} | {matrix_row[index]} | {pdf_row[index]} | {recomputed} | {band_text} |"
            )
    lines += [
        "",
        "Where the two published numbers differ, both stay in the table. Matching bands are an observation about the 4.5 and 3.0 thresholds, not a choice of ratio.",
        "",
        "## Pairs the published light and 暮靄 tables agree on",
        "",
        "Recomputed here, two decimals. These are checks against figures that already match across `contrast-matrix.md` and the whitepaper.",
        "",
        "| Pair | Recomputed | Band |",
        "|---|---|---|",
    ]
    agreed = [
        ("3D3833", "F8F6EF", "ink-1 on 暖紙白"),
        ("6E675E", "F8F6EF", "ink-2 on 暖紙白"),
        ("9C948A", "F8F6EF", "ink-3 on 暖紙白"),
        ("B9DDF1", "F8F6EF", "淺天空藍 on 暖紙白"),
        ("3D3833", "B9DDF1", "ink-1 on 淺天空藍"),
        ("3D3833", "F4DDE7", "ink-1 on 荷花粉"),
        ("3D3833", "CDBFE0", "ink-1 on 淡紫"),
        ("3D3833", "E8E3CC", "ink-1 on 燕麥米"),
        ("3D3833", "B7C8A8", "ink-1 on 鼠尾草綠"),
        ("3D3833", "CBBF9E", "ink-1 on 亞麻金"),
        ("3D3833", "A38E7A", "ink-1 on 可可棕"),
        ("7C9DB5", "1F1B16", "霧靄藍 on bg-0"),
        ("B394A3", "1F1B16", "乾藕粉 on bg-0"),
        ("93879F", "1F1B16", "菸灰紫 on bg-0"),
        ("7C6B59", "1F1B16", "深可可 on bg-0"),
        ("75589D", "F8F6EF", "深藤紫 on 暖紙白"),
        ("75589D", "CDBFE0", "深藤紫 on 淡紫"),
    ]
    for fg, bg, label in agreed:
        value = contrast(fg, bg)
        lines.append(f"| {label} | {value} | {band(value)} |")
    lines += [
        "",
        "## Whitepaper §7.3 figures that this arithmetic does not reproduce",
        "",
        "The whitepaper says the light-theme foreground contrasts of the tentative status colors on 暖紙白 are 3.24, 2.90, and 2.53. Recomputation for 鼠尾草綠, 亞麻金, and 乾藕粉 on `#F8F6EF` is listed below. 3.24 and 2.90 are not those three results. This note does not replace the whitepaper sentence and does not declare the recomputation the winner. It records that the figures were not reproduced for the colors named beside them.",
        "",
        "| Foreground on `#F8F6EF` | Recomputed |",
        "|---|---|",
        f"| `#B7C8A8` | {contrast('B7C8A8', 'F8F6EF')} |",
        f"| `#CBBF9E` | {contrast('CBBF9E', 'F8F6EF')} |",
        f"| `#B394A3` | {contrast('B394A3', 'F8F6EF')} |",
        "",
        "Passing 4.5 is body text. Passing 3.0 and missing 4.5 is large text or a UI boundary. Below 3.0 is decoration. 可可棕 under ink-1 stays in the large-or-boundary band in both published tables and in this check, so it is not a normal body background.",
        "",
    ]
    return "\n".join(lines)


def derived_index(colors: dict[str, str]) -> dict:
    return {
        "kind": "derived-index",
        "originalArchiveContained": {
            "tokens.json": False,
            "tokens.light.json": False,
            "scripts/color_math.py": False,
            "scripts/contrast_verify.py": False,
        },
        "source": "assets/tokens/tokens.css",
        "note": "Built by scripts/validate_wenrun.py from tokens.css. Not an original tokens.json.",
        "colors": [{"token": name, "hex": hx} for name, hx in colors],
    }


def emit() -> None:
    css = (ROOT / "assets/tokens/tokens.css").read_text(encoding="utf-8")
    matrix_text = (ROOT / "assets/tokens/contrast-matrix.md").read_text(encoding="utf-8")
    colors = parse_css_colors(css)
    matrix = parse_matrix_wood(matrix_text)
    (ROOT / "references/contrast-check.md").write_text(contrast_report(matrix), encoding="utf-8")
    (ROOT / "assets/tokens/index.derived.json").write_text(
        json.dumps(derived_index(colors), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("emitted contrast-check.md and index.derived.json")


def check() -> list[str]:
    errors: list[str] = []

    for rel, expected in HASHES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        if expected is not None and sha256(path) != expected:
            errors.append(f"hash changed for verbatim file {rel}")

    css = (ROOT / "assets/tokens/tokens.css").read_text(encoding="utf-8")
    colors = parse_css_colors(css)
    upper = {hx for _, hx in colors}
    for name, hx in LOCKED.items():
        if hx not in upper:
            errors.append(f"locked color missing from tokens.css: {name} {hx}")
    if "b7c8a8" not in css:
        errors.append("tokens.css no longer records the lowercase sage spelling")
    if "75589D" not in upper or "提案" not in css:
        errors.append("深藤紫 must remain present and marked as a proposal in tokens.css")
    by_token: dict[str, list[str]] = {}
    for name, hx in colors:
        by_token.setdefault(name, []).append(hx)
    if by_token.get("--c-wood-cocoa-text") != ["9D8A76"]:
        errors.append("--c-wood-cocoa-text changed")
    if by_token.get("--ink-1") != ["3D3833", "E6E1D5"]:
        errors.append(f"--ink-1 assignments changed: {by_token.get('--ink-1')}")
    if by_token.get("--ink-3") != ["9C948A", "7A7268"]:
        errors.append(f"--ink-3 assignments changed: {by_token.get('--ink-3')}")
    if '"Noto Sans SC Variable"' not in css or "--fs-body: 14px" not in css:
        errors.append("type token drifted from Noto Sans SC Variable / 14px")
    if "--fs-body-mobile: 15px" not in css or "--leading-body: 1.7" not in css:
        errors.append("mobile size or leading drifted")
    if "--wght-shift: -40" not in css or "tabular-nums" not in css:
        errors.append("dark weight or tabular-nums drifted")

    matrix = parse_matrix_wood((ROOT / "assets/tokens/contrast-matrix.md").read_text(encoding="utf-8"))
    if set(matrix) != set(PDF_WOOD):
        errors.append("wood rows missing from contrast-matrix.md")
    report = contrast_report(matrix)
    report_path = ROOT / "references/contrast-check.md"
    if not report_path.exists() or report_path.read_text(encoding="utf-8") != report:
        errors.append("references/contrast-check.md is stale; run scripts/validate_wenrun.py --emit")
    if "does not choose a winner" not in report:
        errors.append("contrast check lost the no-winner statement")
    for hx, pdf_row in PDF_WOOD.items():
        for index, bg in enumerate(DARK_BG):
            if band(matrix[hx][index]) != band(pdf_row[index]) or band(matrix[hx][index]) != band(contrast(hx, bg)):
                errors.append(f"threshold band diverged for {hx} on {bg}; update the prose, do not hide it")

    index_path = ROOT / "assets/tokens/index.derived.json"
    if not index_path.exists():
        errors.append("missing derived index")
    else:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if index.get("kind") != "derived-index":
            errors.append("derived index lost its kind")
        if index.get("originalArchiveContained", {}).get("tokens.json") is not False:
            errors.append("derived index claims tokens.json existed")
        got = [(item["token"], item["hex"]) for item in index["colors"]]
        if got != colors:
            errors.append("derived index does not match tokens.css properties")

    for banned in ("tokens.json", "tokens.light.json", "color_math.py", "contrast_verify.py"):
        if list(ROOT.rglob(banned)):
            errors.append(f"unexpected original-looking file present: {banned}")
    if (ROOT / "research").exists():
        errors.append("research corpus should not be published")
    if list(ROOT.rglob("*Ludi*")):
        errors.append("Ludi study material should not be published")
    if list((ROOT / "assets/tokens").glob("vibe-content.css")):
        errors.append("sticker CSS must not sit in the product token folder")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    meta = frontmatter(skill)
    if meta.get("name") != "ymzz-wenrun-design":
        errors.append(f"skill name is {meta.get('name')}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta.get("name", "")):
        errors.append("skill name is not a lowercase hyphenated token")
    description = meta.get("description", "")
    if not (20 <= len(description) <= 1024):
        errors.append(f"description length {len(description)} is outside 1..1024")
    for needle in ("Use when", "PPTX", "DOCX", "XLSX", "frontend", "backend", "UI"):
        if needle not in description:
            errors.append(f"description missing {needle}")
    if meta.get("license") != "MIT":
        errors.append("skill license must stay MIT")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for hx in LOCKED.values():
        if f"#{hx}" not in readme:
            errors.append(f"README missing locked hex {hx}")
    if "assets/color-card.png" not in readme:
        errors.append("README does not show the color card")
    for label in ("提案", "淺色", "PPTX", "DOCX", "XLSX", "Frontend", "Backend", "UI / UX"):
        if label not in readme:
            errors.append(f"README missing {label}")
    backend = (ROOT / "references/backend-contracts.md").read_text(encoding="utf-8")
    if "does not contain a finished HTTP schema" not in backend:
        errors.append("backend contract must say the archive has no finished HTTP schema")
    if "Derived practical shapes" not in backend:
        errors.append("backend contract must label derived shapes")
    for name in (
        "references/interaction-and-states.md",
        "references/frontend.md",
        "references/backend-contracts.md",
        "references/source/08-跨語言協作.md",
        "references/source/10-體驗底線.md",
    ):
        if not (ROOT / name).exists():
            errors.append(f"missing {name}")
    contract = subprocess.run([sys.executable, str(ROOT / "scripts" / "ux_contract.py")], capture_output=True, text=True)
    if contract.returncode != 0:
        errors.append(contract.stdout + contract.stderr)

    office = (ROOT / "references/office-derivations.md").read_text(encoding="utf-8")
    if "never mentions PPTX, DOCX, or XLSX" not in office:
        errors.append("office file must say the archive never names those formats")
    if "derivation" not in office.lower() and "Derived" not in office:
        errors.append("office file must mark itself as derived")
    if "Noto Sans SC" not in office:
        errors.append("office file drifted off Noto Sans SC")

    card_svg = (ROOT / "assets/color-card.svg").read_text(encoding="utf-8")
    paints = {item.upper() for item in re.findall(r"(?:fill|stroke)=\"#([0-9A-Fa-f]{6})\"", card_svg)}
    allowed = {hx for _, hx in colors} | {"6E675E"}
    if not paints <= allowed:
        errors.append(f"color card uses colors outside tokens.css: {sorted(paints - allowed)}")
    if FORBIDDEN_CARD & paints:
        errors.append("color card includes a non-product color")
    if "75589D" not in paints or "F8F6EF" not in paints or "B7C8A8" not in paints:
        errors.append("color card is missing a required swatch")

    layout = json.loads((ROOT / "assets/color-card.layout.json").read_text(encoding="utf-8"))
    image = Image.open(ROOT / "assets/color-card.png").convert("RGB")
    if image.size != (layout["width"], layout["height"]):
        errors.append("color card PNG size does not match layout")
    for sw in layout["swatches"]:
        cx = sw["x"] + sw["w"] // 2
        cy = sw["y"] + sw["h"] // 2
        pixel = image.getpixel((cx, cy))
        expect = tuple(int(sw["hex"][i : i + 2], 16) for i in (1, 3, 5))
        if pixel != expect:
            errors.append(f"swatch center {sw['name']} is {pixel}, expected {expect}")
        if cx < 32 or cy < 32 or sw["x"] < 32 or sw["y"] + sw["h"] > image.height - 32:
            errors.append(f"swatch clipped: {sw['name']}")

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        errors.extend(markdown_links(path))

    return errors


def main() -> int:
    if "--emit" in sys.argv:
        emit()
    errors = check()
    if errors:
        print("\n".join(errors))
        return 1
    print("wenrun skill checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
