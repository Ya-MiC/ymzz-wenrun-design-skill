# Web visual grammar

These rules are the website grammar. Office files extend them in `office-derivations.md`. They do not get a second aesthetic.

Sourced means the value is in the verified v7.1 files named here. A later catalog such as docs/13 names more fonts; it does not replace the token.

## Type

From `tokens.css`:

| Token | Value |
|---|---|
| `--font-sans` | `"Noto Sans SC Variable", "Noto Sans SC", system-ui, sans-serif` |
| `--fs-body` | `14px` |
| `--fs-body-mobile` | `15px` |
| `--fs-secondary` | `13px` |
| `--fs-caption` | `12px` |
| `--fs-h3` | `20px` |
| `--fs-h2` | `28px` |
| `--leading-body` | `1.7` |
| weights | 400, 500, 600 |
| `--wght-shift` | `0`, and `-40` under `[data-theme="dark"]` |
| numbers | `font-variant-numeric: tabular-nums` on `:root` |

docs/02 and the acceptance notes say mobile long-form reading is 15–16px. The token that exists is 15px. Do not invent a 16px token. 16px remains the top of that prose range.

Dark mode: variable fonts use `font-variation-settings: "wght" var(--wght-body)` with `--wght-body: calc(400 + var(--wght-shift))`. Static fonts, if a variable file is unavailable, drop one step (600→500, 500→400). That fallback is written in `tokens.css`. Do not pick a different family in order to avoid it.

`system-ui` is the last resort in the token. It is not permission to restyle the page as a generic system theme.

No font files are in the archive. Noto Sans SC is SIL OFL 1.1. Do not relicense it. Do not ship a renamed Noto file. If the face is missing, say so.

docs/13, which is a later catalog in the same archive and not the token file, also names Noto Sans TC, 霞鶩文楷, 粉圓, Pretendard, JetBrains Mono, and Sarasa Mono, with OFL and RFN duties. Those are optional catalog faces. They are not the `--font-sans` token. 霞鶩文楷 and 粉圓 are not body text and do not appear together. This package does not include their binaries.

## Spacing, density, size

From `tokens.css`, all multiples of 4 except the type sizes noted above:

| Token | Value |
|---|---|
| `--sp-1` … `--sp-16` | 4, 8, 12, 16, 24, 32, 48, 64 px |
| `--hit` | 48px |
| `--gap-hit` | 8px |
| `--content-max` | 680px |
| `--content-wide` | 1200px |
| `--side-w` / `--side-w-min` | 264px / 68px |
| `--topbar-h` | 52px |
| comfortable control / row / card pad / block gap | 48 / 56 / 24 / 24 px, leading 1.7 |
| compact | 40 / 40 / 16 / 16 px, leading 1.55 |

Compact density changes those measures. It does not change the 14px body floor or the 48px hit target. A 40px compact control still expands its hit area to 48px. Expansion is `(48 − side) / 2`. A 16px icon expands 16px. A 20px icon expands 14px. A 24px icon expands 12px. Do not copy one inset onto every icon.

There is no `--radius` token. `prompts/02` says cards use 16px with the inner radius equal to the outer radius minus the padding. That sentence is a component prompt, not a token. If you use it, cite the prompt. Do not invent other radii.

## Surface and hierarchy

- Layers are surface 0–3 by lightness. Do not separate them with a 1px border. Adjacent layers should stay distinguishable. The archive asks for at least a 4% lightness step.
- One shadow step per layer. Do not stack a border and a shadow.
- Rest shadow: `0 8px 24px rgba(61, 56, 51, .10)`. Float shadow: `0 16px 48px rgba(61, 56, 51, .16)`. Shadows use warm ink, not cold black.
- Glass is `blur(6px)` and no other blur. At most two glass surfaces in one viewport when performance requires the archive's downgrade.
- Inputs use the warm inset: outer `0 1px 2px rgba(61,56,51,.08)` plus inset `0 1px 2px rgba(61,56,51,.06)`. Focus adds a 3px halo. The light halo in the component rule is `rgba(205,191,224,.45)`, which is 淡紫 at 45%. The token `--focus-halo` is warm ink at 45% in light mode and 暮紙白 at 45% in dark mode. Cite which one you use. Do not remove the focus ring.
- Body copy uses `text-wrap: pretty`. Headings of up to three lines use `text-wrap: balance`.
- Inline icons sit at `vertical-align: -0.125em`. Icon sizes are 16, 20, and 24. Stroke is 1.5.
- One primary color mass on a screen. The archive's contract also says original-color area must not exceed 15%. The whitepaper's 60/30/10 sentence is different. Both are recorded in `color-and-contrast.md`.
- Reading width stays within `--content-max` (680px). Do not run paragraphs across the whole viewport.
- Whitespace is part of the hierarchy. The charter in `references/source/11-審美憲章.md` treats empty space as room for attention, not as unused leftover.

## Do

- Put the page on 暖紙白 or, for the formal family, 燕麥米.
- Put cards on the next surface step.
- Put labels on a family-color ground with ink-1 text.
- Keep numbers tabular so columns do not jitter.
- Keep CJK punctuation rules with `line-break: strict` where the archive's contract asks for it.
- Honor `prefers-reduced-motion` by collapsing animation.
- Keep hit targets at 48px even when the glyph is 16px.
- Separate different actions by at least 8px. Merge avatar and name into one target when they go to the same place.

## Don't

- Don't use the eight colors as body text.
- Don't mix 雲箋 and 陶土 on one surface.
- Don't use `#000000` as the page, a cold gray ramp, or a blue-purple gradient.
- Don't add a ninth hue, including a default link blue.
- Don't draw 1px frames to fake depth.
- Don't load the sticker preset.
- Don't take colors from the cover, the emblem drafts, or a component library's default theme.
- Don't shrink body type below 14px to buy density.
- Don't let compact density shrink the hit target.
- Don't clip CJK with `overflow: hidden` or an ellipsis that hides the word. The archive's later notes prefer an ellipsis before a file extension so the extension stays visible; that is a filename rule, not a reason to truncate sentences.

## Components, only where the source states them

| Piece | Sourced behavior |
|---|---|
| Primary button | min 48px. `prompts/02` says warm-ink ground and white text. White is the structural overlay white already used by the surface alphas, not a ninth brand color. |
| Secondary button | surface-2 and ink text |
| Destructive button | 荷花粉 ground and ink text. Not a bright red. |
| Press | at most 50ms, scale 0.97 in the component prompt |
| List row | at least 56px comfortable |
| Disclosure | grid `0fr` to `1fr`, 240ms, ease `cubic-bezier(.16, 1, .3, 1)`. Do not measure height in script. |
| Ink-in | blur 6px to 0, 120ms, 30ms stagger |
| Springs | snap 1200/72, like 500/18, copy 600/22. Do not retune them in place. |
| Z | sticky 10, popover 90, scrim 110, drawer 120, overlay 130, toast 200 |

Toast duration is stated two ways. The contract says `2500ms + ceil((chars − 20) / 20) × 500ms`, capped at 8s. `motion.js` multiplies without `ceil`. Keep both on record. Do not pretend they are the same code.
