# Provenance

Archive inspected: `wenrun-design-system-v7.1`, 83 files, uploaded as `v021-wenrun-design.zip`. The original zip was not modified. Private study material was not copied.

## What is the source of a color

| Item | Source file in v7.1 | Also stated in | Status as written | In this package |
|---|---|---|---|---|
| Eight locked hex values | `tokens/tokens.css` | docs/01, prompts/00, prompts/01, whitepaper v5, both SKILL files | 【鎖定】 | `assets/tokens/tokens.css` |
| 鼠尾草綠 spelling | CSS writes `#b7c8a8`; docs and whitepaper write `#B7C8A8` | same value | locked | both spellings noted |
| 陶土 is light | docs/01; whitepaper chapter 4 corrects the "dark" misreading | prompts/00 says 陶土（淺） | locked as a light family | color card and docs |
| Dark derivative hex | `tokens/tokens.css` | docs/01, whitepaper chapter 5 | see status conflict below | tokens.css |
| Text cocoa `#9D8A76` | `tokens/tokens.css` | whitepaper chapter 5, contrast matrix | 【派生·已驗證】 | tokens.css |
| 深藤紫 `#75589D` | `tokens/tokens.css` | whitepaper chapter 3 | 【提案·待確認】 | not on the locked rows |
| Neutrals | `tokens/tokens.css` | docs/01 §3 | docs/01 【提案·待確認】; CSS 【鎖定·已確認】 | both labels kept |
| Contrast matrix v3.1 | `tokens/contrast-matrix.md` | root SKILL tells reviewers to match this file | matrix says dark pairs were raised to locked | verbatim copy |
| Whitepaper ratios | `docs/色卡白皮書.pdf`, 10 pages, 2026-10-28, producer metadata Z.ai | calls itself the color case record | dark colors 計算已驗證，待三引擎 | `assets/original/color-whitepaper-v5.pdf` |
| Original swatch pages | PDF pages 3, 5, 6, 7 | — | page 5 is the proposal | PNG renders of those pages |
| Type token | `tokens/tokens.css` `--font-sans` | docs/02 | Noto Sans SC Variable, 14px, 1.7, tabular-nums, dark weight −40 | web grammar |
| Spacing and density tokens | `tokens/tokens.css` v7 block | docs/12 prose | token values are in CSS | web grammar |
| Motion numbers | `tokens/tokens.css` and `tokens/motion.js` | root SKILL §5.2 | toast formula disagrees with `motion.js` about `ceil` | both kept |
| 60/30/10 | whitepaper chapter 2 and root SKILL §2.4 | different splits | both wordings kept | color document |
| Office mapping | not in the archive | requested for this skill | derived | `references/office-derivations.md` |
| Interaction and non-ideal states | docs/10, docs/03, docs/09, root contract §5 | verbatim copies of docs/08, docs/09, docs/10 | sourced principles | `references/interaction-and-states.md` |
| Frontend token consumption | tokens.css, docs/08 §3 | root contract §9 | sourced | `references/frontend.md` |
| Error `{code, message}`, client-owned sentences, dual validation, cancel, no fake ETA | docs/08, root contract §8–§9 | — | sourced behavior, no enum list | `references/backend-contracts.md` |
| Pagination, timezone, filter grammar, retry count, audit schema, retention period | root contract says to decide pagination and timestamps before writing | docs/08 does not give the JSON | derived shapes, not archive specifications | `scripts/ux_contract.py` |

## Status conflict, dark derivatives and neutrals

| Label | File | Do not flatten to |
|---|---|---|
| 【衍生·待驗證】 | docs/01 §2 | locked |
| 【鎖定·已驗證】 | tokens.css header for 暮靄 and 暮林 | the only status |
| 計算已驗證，三引擎真機後升鎖定 | whitepaper chapters 1 and 7 | already finished |
| 【計算已驗證·待終鎖】 | root SKILL §2.2 and checklist item 13 | cancelled by the CSS comment |
| 【提案·待確認】 | docs/01 §3 neutrals | locked |
| 【鎖定·已確認】 | tokens.css neutral comment | the only status |

## Files copied verbatim

| Package path | Archive path |
|---|---|
| `assets/tokens/tokens.css` | `tokens/tokens.css` |
| `assets/tokens/contrast-matrix.md` | `tokens/contrast-matrix.md` |
| `assets/tokens/motion.js` | `tokens/motion.js` |
| `assets/original/color-whitepaper-v5.pdf` | `docs/色卡白皮書.pdf` |
| `references/source/01-色彩系統-四套.md` | `docs/01-色彩系統-四套.md` |
| `references/source/02-表面與字體.md` | `docs/02-表面與字體.md` |
| `references/source/11-審美憲章.md` | `docs/11-審美憲章.md` |
| `references/source/prompts-00-主提示詞.md` | `prompts/00-主提示詞.md` |
| `references/source/prompts-01-色彩提示詞.md` | `prompts/01-色彩提示詞.md` |
| `assets/non-product/vibe-content.css` | `tokens/vibe-content.css` |
| `assets/emblem/*.svg` and the draft note | `emblem/` |

`assets/tokens/index.derived.json` and `references/contrast-check.md` were produced in this package. They are not archive files.

## Mentioned, but not in the archive

| Name | Who mentions it | What was found |
|---|---|---|
| `tokens.json` | this package does not pretend it existed | absent |
| `tokens.light.json` | whitepaper §7.4 says to sync it after 深藤紫 is confirmed | absent |
| `scripts/color_math.py` | whitepaper chapter 6 | absent |
| `scripts/contrast_verify.py` | `tokens/contrast-matrix.md` | absent |

## Contrast drift, no winner

暮林 ratios on bg-1 and bg-2 differ between whitepaper table 6-4 and `contrast-matrix.md`. bg-0 ratios agree. 雲箋, 陶土 light pairs, and 暮靄 pairs that this package recomputed agree with the matrix at two decimals. The check file lists every drifted cell beside a fresh WCAG 2.1 recomputation. The recomputation is arithmetic. It does not replace either source.

Where both published numbers fall in the same 4.5 / 3.0 band, the pass or fail call is safe. They do for the drifted 暮林 cells. The ratios themselves are still cited separately.

## Excluded on purpose

| Material | Why |
|---|---|
| `research/Ludi-語料/` | START-HERE and THIRD-PARTY mark it private study. No license to republish. |
| docs/17, docs/19, and the copied vibe-knowledge skill | Built on that private corpus. |
| App source under `app-tauri/` | Product code, not the design grammar. |
| Cover HTML as a palette | Its gold and grays are cover chrome. |
| Sticker CSS as a UI palette | Domain-isolated marketing preset. |
| Emblem colors as UI colors | The draft and the whitepaper decouple the badge. `case1-seal.svg` also contains `#A3848F`, which is not a token. |

## Third parties

See `THIRD-PARTY.md`. The repo license is MIT for this skill. Fonts, icon sets, and the excluded corpus are not relicensed by that MIT grant.
