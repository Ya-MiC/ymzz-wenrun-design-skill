# Color and contrast

Hex values below are the ones that agree across `tokens.css`, `docs/01`, the color prompts, and the v5 whitepaper. Status labels do not agree. This file keeps the labels apart.

English glosses are translations for readers. They are not separate token names.

## Eight locked colors

雲箋 is the light, airy family. 陶土 is the light, formal, earth family. 陶土 is not a dark theme.

| Family | Name | Hex | Role in docs/01 |
|---|---|---|---|
| 雲箋 | 暖紙白 | `#F8F6EF` | 底層表面、大面積留白 |
| 雲箋 | 淺天空藍 | `#B9DDF1` | 標籤、手繪裝飾、資訊類提示 |
| 雲箋 | 荷花粉 | `#F4DDE7` | 輕柔點綴、重點提示、情感類反饋 |
| 雲箋 | 淡紫 | `#CDBFE0` | 過渡色、聚焦光暈、次級裝飾 |
| 陶土 | 燕麥米 | `#E8E3CC` | 淺表面、卡片 |
| 陶土 | 鼠尾草綠 | `#B7C8A8` | 成功態、自然語義、標籤 |
| 陶土 | 亞麻金 | `#CBBF9E` | 高亮、進度、溫和警示 |
| 陶土 | 可可棕 | `#A38E7A` | 深點綴、邊飾、強調文字底 |

`tokens.css` writes 鼠尾草綠 as `#b7c8a8`. That is the same sRGB value as `#B7C8A8`.

One surface uses one family. Four colors is the cap, not a suggestion. Do not add a ninth hue. Neutrals are not part of the four.

## Dark derivatives

These are the Morandi dark versions. They are semantic colors on top of the warm-black surfaces. They are not a new four-color invention, and they are not the page background.

| Family | Name | Hex | Derived from | Dark-mode role in docs/01 |
|---|---|---|---|---|
| 暮靄 | 暮紙白 | `#E6E1D5` | `#F8F6EF` | 深色模式主文字 |
| 暮靄 | 霧靄藍 | `#7C9DB5` | `#B9DDF1` | 資訊標籤、手繪裝飾 |
| 暮靄 | 乾藕粉 | `#B394A3` | `#F4DDE7` | 重點提示、情感反饋 |
| 暮靄 | 菸灰紫 | `#93879F` | `#CDBFE0` | 聚焦光暈、次級裝飾 |
| 暮林 | 夜麥米 | `#D9D3C0` | `#E8E3CC` | 深色模式主文字 |
| 暮林 | 苔蘚綠 | `#7E8E6F` | `#B7C8A8` | 成功態、自然語義 |
| 暮林 | 褐亞麻 | `#9E9073` | `#CBBF9E` | 高亮、進度 |
| 暮林 | 深可可 | `#7C6B59` | `#A38E7A` | 強調文字底、邊飾 |

Text cocoa `#9D8A76` is a derived text variant for 暮林 only. `tokens.css` marks it 【派生·已驗證】. It is not a fifth brand color. 深可可 `#7C6B59` stays the fill and border color. Both the matrix and the whitepaper put it under 4.5:1 on the warm black backgrounds, so it is not body text there. The exact ratios differ; see the check file.

### Status labels that must all remain

| Topic | docs/01 | tokens.css header | Whitepaper v5 | Root contract SKILL §2.2 |
|---|---|---|---|---|
| Dark derivatives | 【衍生·待驗證】 | 【鎖定·已驗證】 | 計算已驗證，真機三引擎複測後才升鎖定 | 【計算已驗證·待終鎖】 |
| Neutrals | 【提案·待確認】 | 【鎖定·已確認】 | 已確認的中性層，列在【鎖定】的說明裡 | used as the text system, with the final-lock checklist still open |

Do not upgrade the pending labels because another file says locked. The device retest on WKWebView, WebView2, and Android WebView is still an open acceptance item in the archive. This package does not claim that retest happened.

## Proposal, not locked

深藤紫 `#75589D` is in `tokens.css` as 【提案·待確認】. The whitepaper recommends it as a same-hue companion of 淡紫 for links, selected state, focus, and readable violet text. It is not part of the eight locked colors. Do not use it as an approved brand color until it is confirmed.

The whitepaper table 3-1 also lists darker candidates `#5C467C`, `#614983`, `#664D89`, `#6B5190`, and `#705496`. Those values are not in `tokens.css`. Do not add them.

## Neutrals

These do not consume a slot in the four.

| Token | Light | Dark | Use |
|---|---|---|---|
| bg-0 | `#F8F6EF` | `#1F1B16` 暖黑 | page ground |
| bg-1 | white at 62% over bg-0 | `#2A241D` | card |
| bg-2 | white at 80% over bg-0 | `#352E25` | raised / hover |
| bg-3 | white at 95% over bg-0 | `#423A2F` | overlay |
| ink-1 | `#3D3833` | `#E6E1D5` | body |
| ink-2 | `#6E675E` | `#B3AC9F` | secondary |
| ink-3 | `#9C948A` | `#7A7268` | placeholder, disabled |
| line-1 | `#3D3833` at 8% | `#E6E1D5` at 10% | quiet separation, not a 1px solid frame |
| scrim | `#3D3833` at 32% | `#000000` at 50% | overlay dimming only |

The dark page ground is warm black `#1F1B16`, not `#000000`. Pure black is reserved for the dark scrim, which is not a shadow and not a page color.

Light bg-1, bg-2, and bg-3 are alpha composites, not extra hex tokens. This package does not publish opaque stand-ins as source colors. If an Office file needs a solid fill, that solid is computed in `references/office-derivations.md` and labeled derived.

## Body text

- Body, secondary, placeholder, and disabled text use the ink tokens.
- The eight original colors are not text colors. The matrix records 淺天空藍 on 暖紙白 at 1.32:1.
- 可可棕 as a fill under ink-1 is 3.70:1 in both the matrix and the whitepaper. That misses 4.5:1. It can be a large-text or boundary case only. It is not a normal body background.
- Labels are a family-color ground plus ink-1. Check the pair. Ink-1 on 淺天空藍, 荷花粉, 淡紫, 燕麥米, 鼠尾草綠, and 亞麻金 is at or above 4.5 in both published tables. Ink-1 on 可可棕 is the 3.70 exception.

## 60 / 30 / 10, two wordings

Do not merge these into one rule.

Whitepaper chapter 2, written for 雲箋:

> 暖紙白佔絕對主導，表面與留白構成畫面的六成；天空藍與荷花粉合計三成；淡紫與深藤紫的高光時刻只佔一成。

That sentence counts 深藤紫 inside the last tenth. 深藤紫 is still a proposal, so this wording must not be used to approve it.

Root contract SKILL §2.4:

> 60% 底色（紙白/燕麥米）＋30% 表面色塊與中性層＋10% 原色點綴。單屏原色面積超過 15% 即違約。

The 60% ground can be 暖紙白 or 燕麥米. The 30% is neutral surface, not 天空藍 plus 荷花粉. The accent cap is stated as 10% and, separately, as a 15% breach line.

## Status colors are tentative

`prompts/01` says a new semantic color must be mapped from the current four, and if that is not enough, stop and ask. It names 成功 → 鼠尾草綠 / 苔蘚綠, 提示 → 淺天空藍 / 霧靄藍, 重點 → 荷花粉 / 乾藕粉.

`docs/01` forbids mixing the two light families on one surface.

Whitepaper §7.3 is explicitly 【待確認】. It borrows 陶土 fills for success and warning on a light theme and uses 乾藕粉 for danger. That cross-family borrow is not an approved status system.

The same section says the light-theme foreground contrasts of those status colors on 暖紙白 are 3.24, 2.90, and 2.53. Recomputation in this package does not reproduce 3.24 or 2.90 for 鼠尾草綠 and 亞麻金 on 暖紙白. The check file cites the figures separately. Either way, those colors are not body text on paper. Do not invent a brighter red or green to "fix" the tentative status row.

## Colors that are not this palette

| Variant | Where it appears | Treatment |
|---|---|---|
| Sticker preset `#ECE9E2`, `#E8443A`, `#F5B301`, `#2B50C8`, `#111111` | `tokens/vibe-content.css` | Marketing only. Not product UI. Not Office. |
| Cover chrome `#F5F5F4`, `#92761F`, `#151513`, `#7E7C74`, `#4E4732` | whitepaper cover HTML | Cover typography. Not the palette. |
| Emblem draft `#A3848F` | `emblem/case1-seal.svg` gradient stop | Not a token. Badge color is decoupled. |
| Whitepaper route-B film colors | docs/18, excluded private corpus | Not tokens. |

## Thresholds used by the sources

The archive states WCAG-style bands: at least 4.5:1 for body text, at least 3:1 for large text (at least 24px, or at least 18.67px bold) and for UI boundaries. Below 3:1 is decoration. This package uses those bands when it reports pass or fail. A pass/fail call is made only when the published numbers and the recomputation fall in the same band. Disagreements inside one band are cited, not averaged.
