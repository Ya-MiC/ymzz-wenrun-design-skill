# Frontend implementation

Apply the same grammar in the interface. The archive's reference shell is Vue 3, TypeScript, and CSS variables. Another view library may be used only if it consumes the same tokens and the same behavior. This package does not include an application.

## Theme

Load `assets/tokens/tokens.css`. Components use `var(--*)`.

| Attribute | Values | Effect |
|---|---|---|
| `data-theme` | omitted, or `dark` | light ground, or warm-black ground and weight −40 |
| `data-palette` | omitted, or `earth`; dark earth uses `wood` | 雲箋, or 陶土 / 暮林 |
| `data-density` | `comfortable` or `compact` | spacing only |

Do not set both families on one surface. Switch the attribute. Do not rewrite colors in script.

`prefers-color-scheme` may select the dark theme. An explicit `data-theme` wins. That priority is the root contract.

## Type and locale

- The font token is `"Noto Sans SC Variable", "Noto Sans SC", system-ui, sans-serif`.
- Body 14px, line-height 1.7, mobile long-form token 15px.
- `font-variant-numeric: tabular-nums` on the root.
- `line-break: strict` for CJK.
- `text-wrap: pretty` on prose and `text-wrap: balance` on short headings.
- User-facing sentences, including errors, are chosen in the client from a stable code. The server does not send the sentence.
- Dates, numbers, and currency use one formatter for the whole product. The archive requires that and does not name the formatter.

docs/13 is a later font catalog. It does not replace `--font-sans`. A Traditional Chinese product that only ships the SC file is a gap the catalog calls out. It is not permission to drop the token.

## Keyboard, focus, contrast, motion

- Every control is reachable by keyboard. The focus ring is the token ring. Do not set `outline: none` without the replacement ring.
- The focus ring must cover the 48px hit area, not only a 16px glyph.
- Contrast follows `color-and-contrast.md`. Body pairs are at least 4.5:1. Large text and UI boundaries are at least 3:1. Where the whitepaper and the matrix disagree, cite both.
- `prefers-reduced-motion: reduce` collapses animation, including the ink-in effect.
- Glass blur is 6px, and at most two glass surfaces in one viewport when the archive's performance downgrade applies.
- Icon stroke is 1.5. Sizes are 16, 20, and 24. Inline icons use `vertical-align: -0.125em`.

## Components

Build from the sourced patterns in `web-grammar.md` and `interaction-and-states.md`.

- Buttons are at least 48px. Width comes from content and padding, not a fixed width that breaks a longer locale.
- Inputs use the warm inset shadow. Height is 48px in the component prompt.
- Overlays use the sourced names and the z scale in `tokens.css`.
- Tables and charts follow the family palette. Do not import a chart library's default series colors.

## Checks before delivery

Use `references/source/09-驗收清單.md` for the archive's own list. At minimum:

- No hex in component styles except the token file.
- Text uses ink. The eight colors are not body text.
- One family on the screen.
- Hit targets are 48px and do not overlap.
- Focus, Escape, scrim, and close all dismiss an overlay, and the scrim still catches clicks while it is leaving.
- Loading, empty, error, and recovery exist.
- Reduced motion is honored.
- 320px width and 200% zoom do not clip.
- Say which of behavior, visual, accessibility, and device was not tested.

## Not in this package

No Vue app, no icon font build, and no font binaries. A helper for API payloads is `scripts/ux_contract.py`. It does not render UI.
