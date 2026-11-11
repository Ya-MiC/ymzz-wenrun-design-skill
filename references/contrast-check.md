# Contrast check

This file is arithmetic from this package. It is not `scripts/color_math.py` and not `scripts/contrast_verify.py`. Those files are named in the whitepaper and in `contrast-matrix.md`, and they were not in the v7.1 archive.

Method: WCAG 2.1 relative luminance, rounded half up to two decimals. The result is a check. It does not replace either published table and it does not choose a winner.

## 暮林 bg-0 / bg-1 / bg-2

Backgrounds are `#1F1B16`, `#2A241D`, `#352E25`.

| Hex | Stop | contrast-matrix.md | whitepaper table 6-4 | recomputed here | bands |
|---|---|---|---|---|---|
| `D9D3C0` | bg-0 | 11.44 | 11.44 | 11.44 | body |
| `D9D3C0` | bg-1 | 10.15 | 10.25 | 10.25 | body |
| `D9D3C0` | bg-2 | 8.78 | 8.94 | 8.94 | body |
| `7E8E6F` | bg-0 | 4.88 | 4.88 | 4.88 | body |
| `7E8E6F` | bg-1 | 4.34 | 4.37 | 4.37 | large-or-boundary |
| `7E8E6F` | bg-2 | 3.79 | 3.82 | 3.82 | large-or-boundary |
| `9E9073` | bg-0 | 5.45 | 5.45 | 5.45 | body |
| `9E9073` | bg-1 | 4.83 | 4.89 | 4.89 | body |
| `9E9073` | bg-2 | 4.21 | 4.26 | 4.26 | large-or-boundary |
| `7C6B59` | bg-0 | 3.35 | 3.35 | 3.35 | large-or-boundary |
| `7C6B59` | bg-1 | 3.01 | 3.00 | 3.00 | large-or-boundary |
| `7C6B59` | bg-2 | 2.62 | 2.62 | 2.62 | decoration |
| `9D8A76` | bg-0 | 5.16 | 5.16 | 5.16 | body |
| `9D8A76` | bg-1 | 4.63 | 4.63 | 4.63 | body |
| `9D8A76` | bg-2 | 4.04 | 4.04 | 4.04 | large-or-boundary |

Where the two published numbers differ, both stay in the table. Matching bands are an observation about the 4.5 and 3.0 thresholds, not a choice of ratio.

## Pairs the published light and 暮靄 tables agree on

Recomputed here, two decimals. These are checks against figures that already match across `contrast-matrix.md` and the whitepaper.

| Pair | Recomputed | Band |
|---|---|---|
| ink-1 on 暖紙白 | 10.72 | body |
| ink-2 on 暖紙白 | 5.16 | body |
| ink-3 on 暖紙白 | 2.77 | decoration |
| 淺天空藍 on 暖紙白 | 1.32 | decoration |
| ink-1 on 淺天空藍 | 8.10 | body |
| ink-1 on 荷花粉 | 9.02 | body |
| ink-1 on 淡紫 | 6.69 | body |
| ink-1 on 燕麥米 | 8.99 | body |
| ink-1 on 鼠尾草綠 | 6.53 | body |
| ink-1 on 亞麻金 | 6.34 | body |
| ink-1 on 可可棕 | 3.70 | large-or-boundary |
| 霧靄藍 on bg-0 | 5.99 | body |
| 乾藕粉 on bg-0 | 6.26 | body |
| 菸灰紫 on bg-0 | 5.06 | body |
| 深可可 on bg-0 | 3.35 | large-or-boundary |
| 深藤紫 on 暖紙白 | 5.34 | body |
| 深藤紫 on 淡紫 | 3.33 | large-or-boundary |

## Whitepaper §7.3 figures that this arithmetic does not reproduce

The whitepaper says the light-theme foreground contrasts of the tentative status colors on 暖紙白 are 3.24, 2.90, and 2.53. Recomputation for 鼠尾草綠, 亞麻金, and 乾藕粉 on `#F8F6EF` is listed below. 3.24 and 2.90 are not those three results. This note does not replace the whitepaper sentence and does not declare the recomputation the winner. It records that the figures were not reproduced for the colors named beside them.

| Foreground on `#F8F6EF` | Recomputed |
|---|---|
| `#B7C8A8` | 1.64 |
| `#CBBF9E` | 1.69 |
| `#B394A3` | 2.53 |

Passing 4.5 is body text. Passing 3.0 and missing 4.5 is large text or a UI boundary. Below 3.0 is decoration. 可可棕 under ink-1 stays in the large-or-boundary band in both published tables and in this check, so it is not a normal body background.
