# Office derivations

Word, PowerPoint, and Excel are three surfaces of the same grammar. They are not the whole skill. UI, frontend behavior, and backend contracts are specified beside this file. The v7.1 archive never mentions PPTX, DOCX, or XLSX. Everything in this file is a derivation so those formats can carry the same website grammar. It is not a second palette and not an original master file.

Generated samples, still derivations, live in `samples/`. They are 雲箋 only. They are not original masters, and they do not add a ninth hue. `scripts/build_office_samples.py` writes them. If Noto Sans SC is not installed, the reading program may substitute another face. That substitution is not a second specified typeface.

## What stays identical

- The same family for the whole file. 雲箋 or 陶土. 陶土 stays a light theme. Dark files use 暮靄 or 暮林 on `#1F1B16` and the dark surface steps.
- The same eight locked hex values, the same neutrals, the same ban on a ninth hue.
- Body text in ink. Accents are fills, rules, and label chips, not paragraph color.
- 深藤紫 stays unused unless the proposal is confirmed. Links are ink plus an underline. That is a gap, not a hidden blue.
- Status red, amber, and green are not added. Tentative status mappings stay tentative.
- Sticker, cover, and emblem colors stay out.
- The type family remains Noto Sans SC. The token names `"Noto Sans SC Variable"` and `"Noto Sans SC"`. In OOXML, set the typeface to `Noto Sans SC`. That spelling is the same family, not a new choice. If the font is not installed, say that Office substituted something else. Do not write Calibri, 微軟正黑體, or PingFang into the theme and call it the source face.
- Numbers should use a tabular face when one is installed. The archive names JetBrains Mono and Sarasa Mono SC for code figures. Spreadsheet applications do not honor `font-variant-numeric`. If no tabular face is present, state that gap. Do not invent a font.
- No font file is embedded here. OFL licenses are not changed by this package.

## Unit conversion, derived

The archive speaks in CSS pixels. This conversion assumes the CSS definition 96px = 1in = 72pt, so 1px = 0.75pt. It is not an archive token.

| CSS token | px | Derived pt |
|---|---|---|
| body | 14 | 10.5 |
| mobile long-form token | 15 | 11.25 |
| secondary | 13 | 9.75 |
| caption | 12 | 9 |
| h3 | 20 | 15 |
| h2 | 28 | 21 |
| sp-1 … sp-16 | 4, 8, 12, 16, 24, 32, 48, 64 | 3, 6, 9, 12, 18, 24, 36, 48 |
| hit target | 48 | 36 |
| content max | 680 | 510 |
| card pad comfortable / compact | 24 / 16 | 18 / 12 |
| line-height | 1.7 | multiple 1.7 |

docs/12 mentions a meeting display filter of type +20% and stronger contrast, and says the token was never created. It is not in `tokens.css`. Do not invent the missing token. A deck that applies +20% must be labeled as that unfinished filter, not as a sourced slide scale. Do not replace the scale with a generic 32pt title system.

680px does not fit a 13.333in × 7.5in slide as a column. On a slide, keep the same spacing steps and the same one-column hierarchy, and let the slide margins be at least 36pt (the 48px step). Do not stretch a paragraph across the slide.

## Solid fills, derived

Light cards in CSS are white at 62%, 80%, and 95% over `#F8F6EF`. The archive does not publish opaque hex for those layers. Office theme slots need solids. Compositing the stated alphas, rounded to 8-bit, gives:

| Layer | Recipe in tokens.css | Derived solid |
|---|---|---|
| bg-1 | white 62% over `#F8F6EF` | `#FCFCF9` |
| bg-2 | white 80% over `#F8F6EF` | `#FEFDFC` |
| bg-3 | white 95% over `#F8F6EF` | `#FFFFFE` |
| line-1 | `#3D3833` at 8% over `#F8F6EF` | `#E9E7E0` |

These solids are derived. They are not new brand colors. On paper they are very quiet, which matches the source. If a printer drops the step, do not "fix" it with a gray border or a new color. Use the warm shadow, or move to the next sourced dark surface when the file is a dark theme. Dark surfaces already have solid hex values: `#1F1B16`, `#2A241D`, `#352E25`, `#423A2F`.

## Theme slots

Map slots onto the active family. Unused accent slots repeat a family color. They do not receive a new hue.

雲箋, light:

| Slot | Hex | Role |
|---|---|---|
| dk1 / tx1 | `#3D3833` | text |
| lt1 / bg1 | `#F8F6EF` | page |
| dk2 | `#6E675E` | secondary text |
| lt2 | `#FCFCF9` | derived card solid |
| accent1 | `#B9DDF1` | information chip |
| accent2 | `#F4DDE7` | emphasis chip |
| accent3 | `#CDBFE0` | halo, decoration |
| hlink | none approved | ink plus underline |

陶土 replaces the page with `#E8E3CC` and the accents with `#B7C8A8`, `#CBBF9E`, `#A38E7A`. Do not use `#A38E7A` as a small-text background.

Dark 暮靄: page `#1F1B16`, text `#E6E1D5`, secondary `#B3AC9F`, accents `#7C9DB5`, `#B394A3`, `#93879F`. Cards use `#2A241D`, `#352E25`, `#423A2F`. 菸灰紫 is not body text on bg-2 or bg-3; both published tables put it under 4.5 there.

Dark 暮林: accents `#7E8E6F`, `#9E9073`, and text cocoa `#9D8A76`. Fills that want cocoa use `#7C6B59`, not the text variant.

Example, 雲箋 light, OOXML sRGB, derived mapping:

```xml
<a:srgbClr val="3D3833"/>
<a:srgbClr val="F8F6EF"/>
<a:srgbClr val="6E675E"/>
<a:srgbClr val="FCFCF9"/>
<a:srgbClr val="B9DDF1"/>
<a:srgbClr val="F4DDE7"/>
<a:srgbClr val="CDBFE0"/>
```

## PPTX

- One idea a slide. Paper or oat ground. Accent area stays a chip, a bar, or a small label, not a full-bleed rainbow.
- Title is ink, at the h2 step (21pt) unless you explicitly label the unfinished +20% filter.
- Body is ink at 10.5pt, multiple 1.7. Do not autofit below that.
- Margins at least 36pt. Align to the spacing steps.
- Keep text in text frames. Do not draw the slide as one picture.
- If the copy does not fit, add a slide. Do not shrink type and do not ellipsize a sentence.
- Titles wrap to at most two lines. Do not clip the descenders.
- Charts use only the active family's chromatic colors, in source order. 雲箋 has three chromatic colors besides paper. A fourth series is a gap: use ink-2 as a neutral series or split the chart. Do not invent a series color.
- Axis text and legends are ink. Gridlines use the derived line solid or no line. Do not add a blue grid.
- The 48px hit rule is for interactive controls. It is not a reason to make every decorative mark 36pt tall.

## DOCX

- Page color is the family ground when the format allows it.
- Normal: Noto Sans SC, 10.5pt, ink-1, line multiple 1.7.
- Heading 2: 21pt, weight 600, ink-1. Heading 3: 15pt, ink-1. Caption: 9pt, ink-2.
- Do not color a heading with 淺天空藍 or 荷花粉.
- A label chip may use a family fill with ink-1 text, as on the web.
- Margins at least 36pt. Keep headings with the next paragraph so they do not sit alone at the bottom.
- Tables: header fill is a family chip that passes 4.5:1 with ink-1. 可可棕 does not. Cell text is ink. Quiet gridlines may use the derived line solid; a heavy grid is not the web grammar. The archive allows platform-native table rules as an exception to the no-border rule. Do not invent a darker grid color.
- Do not put text in a floating box that clips. Let the table grow. Do not shrink body type to fit a cell.
- Print: repeat header rows, and do not rely on a background image. If a printer drops the page tint, the ink-on-white result is still readable because body text is ink. Say that the tint was lost. Do not recolor the type to compensate.

## XLSX

- Workbook theme uses the same slot map.
- Header row: family chip plus ink-1, 10.5pt, not bold color text. Freeze that row.
- Data text is ink-1. Zebra fills, if needed, use the derived card solid or the next surface. Not a new gray.
- Wrap text. Widen columns instead of showing `#####` or an ellipsis that hides the value. Row height follows the line, not the 48px hit target. A button placed on a sheet still needs a 48px target; a data cell does not.
- Numbers are right-aligned. Dates and currency keep a consistent format down the column so the tabular intent survives even when the font cannot.
- Charts follow the PPTX series rule.
- Print: fit to width, repeat the header row, margins at least 36pt. Do not scale the sheet so body type falls below 10.5pt.
- One family for the workbook. A second family means a separate sheet, with a neutral break, and it must be labeled. Do not mix them in one table.

## Overflow, truncation, print

| Format | Faithful behavior | Derived adaptation |
|---|---|---|
| Web | `text-wrap: pretty`, balanced headings, 14px floor, no clipped CJK | none |
| PPTX | same type scale and ink | extra slides instead of autofit; 36pt margins |
| DOCX | same type scale and ink | keep-with-next; table grows instead of clipping |
| XLSX | ink, family header chip | wrap and widen; do not treat rows as hit targets |

If a value is missing, leave the gap in the file notes. Do not backfill it.
