# Interaction, states, and responsive UI

One visual grammar covers web, desktop, and mobile. Word, PowerPoint, and Excel use the same colors, type, and hierarchy through `office-derivations.md`. They do not replace this interaction model, and this model does not replace them.

The archive's own shell is Tauri, Vue, and Rust. The rules below are the reusable behavior. File paths in `references/source/08-跨語言協作.md` are that shell's layout, not a requirement to create one.

## Sourced

| Concern | Rule | Where |
|---|---|---|
| Structure | Navigation follows the person's task. Similar tasks share one page skeleton. | docs/10 §17 |
| Recognition | Options are visible. A core task is not hidden behind memory. | docs/10 §18 |
| Forms | The unit is the whole journey: input, understand, validate, submit, recover. | docs/10 §19 |
| Non-ideal states | Deliver loading, empty, error, offline, no-permission, partial success, cancel, and recovery with the normal screen. | docs/10 §20–21 |
| Recovery | Undo, save, and restore matter more than a comforting animation. | docs/10 §21 |
| Input parity | Keyboard, mouse, and touch can all finish a core task. | docs/10 §22 |
| Place | Do not move the thing the person is operating, and do not steal the reading position, unless they asked. | docs/10 §23, docs/03 scroll rule |
| Density | Comfortable and compact are independent of the color family. Compact does not scale everything down. Body stays 14px. Hit targets stay 48px. | docs/10 §24, `tokens.css` |
| Tables | Reuse a mature table behavior. The product owns column meaning, priority, readability, and brand. | docs/10 §25 |
| Data format | Text, numbers, dates, and locale are system rules, not per-page choices. Numbers are tabular. | docs/10 §26, `tokens.css` |
| Files | Prefer the platform's own file behavior. Branding does not mean redrawing every native action. | docs/10 §27 |
| Hit target | Visual size may be 16px. The hit target is at least 48×48 CSS px. Expansion is `(48 − side) / 2`. Different actions stay at least 8px apart. | `tokens.css`, docs/03 |
| Focus | 2px outline in the accent plus a 3px halo. Never remove it. Return focus to the trigger when an overlay closes. | `tokens.css` |
| Motion | Honor `prefers-reduced-motion`. Disclosure uses grid `0fr` to `1fr`. | `tokens.css` |
| Transparency | `prefers-reduced-transparency` drops blur to 0 and raises surface opacity. The archive does not publish the raised opacity value. | root contract §5.5 |
| Contrast preference | `prefers-contrast: more` deepens ink. The archive does not publish the deepened hex. Do not invent one. | root contract §5.5 |
| Zoom | 200% text and 200% page zoom do not clip, overlap, or shrink hit targets, and do not force a horizontal scroll. | docs/09, root contract §5.5 |
| Status | Success, warning, and error are not color alone. Add icon and text. The status hues themselves are still tentative. | root contract §5.5 |
| IME | While composing, Enter confirms a candidate and does not submit. Global shortcuts pause. | docs/03 |
| Scroll | Leave the bottom when the person scrolls up. Show a return control. Resume only within 48px of the bottom. | docs/03 |
| Loading | Prefer a skeleton. Show a percent only when progress is measurable. No fake ETA. A task longer than 10s can be cancelled. | root contract §5.4, docs/08 |
| Overlays | Name the pattern. Modal, alert dialog, popconfirm, drawer, sheet, toast, snackbar, inline alert, tooltip, popover, menu, tour, lightbox, loading. Four dismiss paths share one dirty-state guard. The scrim keeps hits during the exit. | root contract §5.4 |
| Back | Top overlay, then the edit guard, then route back, then a second press to leave the root. | prompts/05 |
| Breakpoints | Narrow under 480, medium 480–833, wide 834–1199, extra wide 1200–1919, full at 1920. Components use container queries. Only the app shell uses the viewport. 320px still works. | docs/12 |
| Checks | Split evidence into behavior, visual, accessibility, and device. Say what was not tested. | docs/10 §29, `references/source/09-驗收清單.md` |

## Forms

1. Label every field in text. Placeholder is not the label.
2. Validate on the client for immediate feedback and again on the server. The client check is not the security check. That split is sourced.
3. Map a stable error code to a sentence on the client. Do not invent a red that is not in the active family.
4. Recover the person's input after a failure. Do not clear the form.
5. Use the platform input type and autocomplete the archive already names where they fit: telephone uses `tel`, a one-time code uses `one-time-code`. Other autocomplete values are not listed. Do not invent a new one and call it sourced.
6. Keep the 48px target on the submit control. Compact density does not remove it.

## Navigation

- The person can tell where they are and what going back will restore.
- Side navigation uses the sourced widths: 264px open, 68px collapsed. If the open side would leave the main area under 600px, collapse it. Those widths are tokens.
- Do not introduce a second navigation pattern for the same task on a phone. Orientation rearranges. It does not unlock a hidden feature. That is the archive's docs/12 rule.

## Tables and charts

- Header fill is a family chip with ink text. 可可棕 is not a small-text header.
- Wrap text. Do not ellipsize the value that identifies a row.
- Zebra, if needed, uses the next surface step, not a new gray.
- Chart series use only the active family's chromatic colors. 雲箋 has three besides the ground. A fourth series is a gap: use ink-2 or split the chart. Do not add a hue.
- On a narrow viewport, keep the comparison readable. Enlarge touch targets. Do not shrink the chart into an unreadable thumbnail and call that responsive.

## Empty, error, offline, recovery

Each of these is a designed state, not a leftover string:

| State | Minimum content |
|---|---|
| Loading | Skeleton or a real progress value. No invented ETA. |
| Empty | One sentence and one next action. The archive's component prompt also allows a quiet illustration in 淺天空藍 or 荷花粉. |
| Error | What failed, the stable code's mapped sentence, and a way to retry or go back. Do not pretend success. |
| Offline | What still works locally. Do not show a fake synced state. |
| No permission | Say so. Do not render an empty success. |
| Partial success | Name what finished and what did not. |
| Cancel | Stop the task and keep what the person already entered. |
| Recovery | Undo or restore when the action destroys data. |

## Derived, and labeled as such

- Office files do not implement hit targets, focus order, or IME. Their derivation is color, type, spacing, and editable text. See `office-derivations.md`.
- A component library's default blue, red, and gray is not a sourced state color.
- `prefers-contrast` has no published hex step. Leave it unimplemented rather than darkening ink by an unstated amount.
