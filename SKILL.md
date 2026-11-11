---
name: ymzz-wenrun-design
description: >-
  Applies the 晏銘湛箴 (ymzz) wenrun grammar, the approved 稟冊 v0.21 look,
  across UI and UX for web, desktop, and mobile, frontend implementation,
  and the backend contracts that support that UX, plus editable Word DOCX,
  PowerPoint PPTX, and Excel XLSX. Use when designing or reviewing
  interfaces, onboarding, components, states, forms, tables, charts,
  tokens, accessibility, API errors, progress, or validation that must
  keep one visual and interaction logic. Concrete Office mappings and API
  schemas the archive does not define are derivations. Do not use for an
  unrelated visual system.
license: MIT
---

# 晏銘湛箴 / ymzz wenrun design

Use this skill for the whole product surface, not for a palette PDF alone and not for Office alone.

- UI and UX on the web, on the desktop, and on a phone
- Frontend implementation: tokens, theme, components, keyboard, focus, contrast, motion, and locale
- Backend contracts that support that UX: errors, validation, progress, cancel, privacy
- Editable Word (DOCX), PowerPoint (PPTX), and Excel (XLSX)

The grammar comes from wenrun-design-system v7.1. The approved product picture of that grammar is 稟冊 v0.21 (`ymzz-bingce`), commit `4d59b866` on `cursor/v021-integrated-app-e023`. Its `app/ui/tokens.css` is byte-identical to `assets/tokens/tokens.css`. Radius, the compact density switch, and the undefined `--paper` reference live in `app/ui/app.css` and are recorded in `references/product-playbook.md`. They are not new locked colors.

It is not a Tailwind, Ant Design, or default Office theme. The backend section is not a server color scheme. This package does not ship the 稟冊 application, a checkout, or a hosted API.

The skill is generic. It does not assume a particular chat, bot, or application shell.

## Authority

Follow this order when sources disagree. Do not collapse a disagreement into one "approved" value.

1. **Color values that were actually in the archive.** `assets/tokens/tokens.css` is the only machine-readable color file. There was no `tokens.json` and no `tokens.light.json`.
2. **Role sentences.** `references/source/01-色彩系統-四套.md`, the color prompts, and `assets/original/color-whitepaper-v5.pdf`.
3. **Status labels stay as written.** Dark derivatives and neutrals carry contradictory labels. Keep all of them. Do not promote a proposal, and do not treat a "locked" comment as cancelling a "pending device check" label.
4. **Contrast arithmetic in this package is a check, not a fourth source of truth.** Where the whitepaper and `assets/tokens/contrast-matrix.md` print different ratios, cite both. Do not pick a winner. See `references/contrast-check.md`.
5. **Interaction.** `references/interaction-and-states.md` and the verbatim copies of docs/08, docs/09, and docs/10. Breakpoints and overlay names that live only in the archive are cited there. Do not add a state color.
6. **Office files.** `references/office-derivations.md` is a derivation so Word, PowerPoint, and Excel can use the same grammar. The v7.1 archive never mentions PPTX, DOCX, or XLSX.
7. **Backend payloads.** The archive requires stable error codes, client-owned sentences, a second validation, cancel, and measurable progress. It does not define pagination, timezone, retry count, or a retention period. Those shapes in `references/backend-contracts.md` are derived. Do not describe them as original specifications.

## Procedure

1. Read `assets/tokens/tokens.css` before choosing a color. Consume variables on the web. Do not sprinkle new hex values.
2. Choose one family for the whole surface.
   - Light, airy, younger: **雲箋**. Its dark companion is **暮靄**.
   - Light, formal, earthy: **陶土**. 陶土 is a light palette, not a dark theme. Its dark companion is **暮林**.
3. Use at most that family's four colors. Neutrals do not count toward the four. Do not add a hue.
4. Put body text in ink only. Light ground: `#3D3833`, secondary `#6E675E`. Dark ground: `#E6E1D5`, secondary `#B3AC9F`. `#9C948A` and `#7A7268` are placeholder and disabled text only.
5. Do not set 雲箋 or 陶土 colors as text. Do not put body text on 可可棕 `#A38E7A`. On a dark ground, do not write with 深可可 `#7C6B59`; the derived text cocoa is `#9D8A76`, and it is not a fifth brand color.
6. Keep one family on one surface. If two zones are required, separate them with neutrals. Do not blend 雲箋 into 陶土.
7. Set type from the token, not from a generic substitute: `"Noto Sans SC Variable", "Noto Sans SC", system-ui, sans-serif`. Body `14px`, line-height `1.7`, `tabular-nums`. The mobile long-form token is `15px`; the prose range `15–16px` is the document sentence, not a second token. Dark mode shifts variable-font weight by `-40`.
8. For a product surface, follow `references/product-playbook.md` and `references/product-recipes.md`. Nickname first. No typed paths. Numbers and cards open their detail. Sidebar, breadcrumbs, and `Cmd/Ctrl+K` are the bar. 稟冊 v0.21 has the nickname screen and the sidebar. It does not yet have breadcrumbs, a command palette, or clickable report numbers. Do not describe those gaps as finished.
9. For UI on web, desktop, or mobile, also follow `references/interaction-and-states.md` and `references/frontend.md`. Cover loading, empty, error, offline, permission, partial success, cancel, and recovery. Keep keyboard, pointer, and touch able to finish the task. On a phone, do not copy the v0.21 sticky `100vh` sidebar.
10. For a backend or adapter, follow `references/backend-contracts.md`. Keep the sourced behavior. Use a derived JSON shape only when the archive has no shape, and say so. Do not paint the API in brand colors. Do not send a translated sentence as the error body.
11. For Word, PowerPoint, or Excel, follow `references/office-derivations.md`. Match the generated 雲箋 files in `samples/` or say which decision differs. Deliver editable text, styles, and cells.
12. If a needed value is not in the source, stop and name the gap. Do not fill it with a default blue, a new status red, an unstated retry count, or an unstated size.

## Hard rules

- Four colors per set. The eight locked values are in `references/color-and-contrast.md`.
- `#75589D` 深藤紫 is a proposal waiting for confirmation. It is not locked.
- Status-color semantics are tentative. Do not invent a traffic-light red, amber, and green.
- Badge and emblem colors are independent of the UI palette. Do not copy them back into the interface.
- `assets/non-product/vibe-content.css` is a marketing sticker preset. Do not load it for product UI or Office files.
- The whitepaper cover's gold and gray are cover chrome, not the palette.
- `research/Ludi-語料/` was marked private study. It is not in this package. Do not recreate it.

## Reference index

| File | What it is |
|---|---|
| `assets/color-card.png` | Readable card of the source hex values. A keyline is drawn only so a chip can be seen; the keyline is not a color. |
| `assets/color-card.svg` | Same card, vector. |
| `assets/original/color-whitepaper-v5.pdf` | Original 10-page whitepaper. Swatches: page 3 雲箋, page 5 深藤紫 proposal, page 6 陶土, page 7 暮靄 and 暮林. |
| `assets/tokens/tokens.css` | Verbatim machine source. |
| `assets/tokens/contrast-matrix.md` | Verbatim v3.1 matrix. |
| `assets/tokens/index.derived.json` | Index built here from `tokens.css`. Not an original file. |
| `references/color-and-contrast.md` | Roles, status conflicts, 60/30/10 wording, contrast. |
| `references/contrast-check.md` | Recomputation beside the two published tables. No winner. |
| `references/product-playbook.md` | How to build the product. 稟冊, T3 Code, Nowledge Mem. Gaps kept visible. |
| `references/product-recipes.md` | Page and component recipes, with screenshots of the v0.21 UI. |
| `references/web-grammar.md` | Type, spacing, density, hierarchy, components, do and don't. |
| `samples/` | Generated 雲箋 PPTX, DOCX, and XLSX. Derivations, not masters. |
| `assets/product/bingce-app.css` | Verbatim 稟冊 v0.21 chrome. Not a second palette. |
| `references/interaction-and-states.md` | Forms, navigation, tables, charts, loading, empty, error, recovery, responsive behavior. |
| `references/frontend.md` | Tokens, theme, keyboard, focus, contrast, motion, locale, delivery checks. |
| `references/backend-contracts.md` | Sourced error and task rules, then derived payloads. Not a color theme. |
| `references/office-derivations.md` | Word, PowerPoint, and Excel. Derived. |
| `scripts/ux_contract.py` | Tests the derived error, progress, and page shapes. |
| `references/provenance.md` | Source-of-truth table. |
| `references/source/` | Verbatim copies of the design documents used here, including docs/08, docs/09, and docs/10. |

## Gaps that must stay gaps

- No original `tokens.json`, `tokens.light.json`, `scripts/color_math.py`, or `scripts/contrast_verify.py`. The whitepaper and the matrix mention the scripts. The files were not in the archive.
- No font binaries. Do not relicense OFL fonts by embedding them without their license.
- No device retest across WKWebView, WebView2, and Android WebView. Several status labels exist because that retest was still open.
- No original slide, page, or worksheet master. Office sizes in the derivation file are conversions, not archive tokens.
- No original pagination schema, timestamp format, filter grammar, retry count, audit log, or retention period. docs/08 and the root contract require those conventions to be decided. They do not decide them.
- No published hex step for `prefers-contrast: more`, and no published opacity for `prefers-reduced-transparency`.
- No application, hosted API, checkout, or paid service is part of this package.
- No `--radius` token and no `--paper` token. 12px and 16px are chrome measurements from `app.css`. `--paper` is an unresolved reference.
- No command palette, breadcrumb, or clickable report number in the captured 稟冊 v0.21 UI. The playbook requires them for new work.
