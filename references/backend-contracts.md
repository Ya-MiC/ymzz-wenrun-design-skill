# Backend contracts

The backend is not a color theme. These contracts exist so the interface can stay honest: errors map to sentences, long tasks can be cancelled, and the person can tell what was stored.

The archive does contain some of this. It does not contain a finished HTTP schema. The split below is the point.

## Sourced requirements

From `references/source/08-跨語言協作.md`, the root contract §7–§9, and docs/10.

| Requirement | What the archive actually says | What it does not say |
|---|---|---|
| Error shape | `{code, message}`. `code` is an enum. The client maps the code to a sentence. The server does not send that sentence and does not return a bare string. | The enum members. The meaning of `message` beyond "not the user sentence". |
| Field names | `snake_case`. | A full resource list. |
| Validation | The client checks for feedback. The server checks again and does not trust the client. | The field-level rule language. |
| Pagination and time | "Decide the pagination and timestamp convention before writing." | Cursor versus page, page size, and the timestamp format. |
| Long tasks | Progress events and cancel. A percent only when progress is measurable. No fake ETA. Longer than 10s must be cancellable. | The event JSON. A retry count. |
| Failure honesty | Do not pretend success. A mock uses the same codes as the real boundary. | — |
| Files | Write a temp file, then replace atomically. Prefer platform file behavior. | An upload protocol. |
| Idempotency | A command is idempotent or it is marked otherwise. | Which commands those are. |
| Privacy | Local-first. Cloud sync is optional. Collect less. Statistics the product keeps are visible on the device and clearable in one action. The UI does not hold keys. | A retention period in days. An audit-log schema. A regulation checklist. |
| Adapters | The archive's own boundary is Rust IPC plus an optional Python sidecar that speaks JSON lines. Panic does not cross that boundary. | A universal HTTP framework. |

The archive's reference implementation names `AppError`, `invoke`, Vue on one side, and Rust on the other. Those names are the shell they wrote. A different runtime still has to keep the sourced behavior: stable codes, client-owned sentences, a second validation, cancel, and measurable progress.

## Derived practical shapes

These shapes are defined here so an implementation has something testable. They are not in the v7.1 archive. `scripts/ux_contract.py` checks them. If a project already chose another shape, keep the sourced behavior and do not pretend that other shape is the archive.

### Error envelope

```json
{"code": "not_found", "message": "not_found"}
```

- `code` and `message` are snake-case tokens from the project's enum.
- `message` repeats a stable token. It is not a translated sentence. That constraint is a practical reading of "the server does not send user copy". The archive did not say the token must equal `code`.
- Do not add `user_message`, `localized_message`, or a nested copy object.
- Keys are snake case.

### Progress event

```json
{"task_id": "export_1", "state": "running", "completed": 2, "total": 5, "cancellable": true}
```

- `state` is one of `queued`, `running`, `succeeded`, `failed`, `cancelled`. Those five names are derived.
- `total` is null when the length is unknown. Then omit any percent.
- No `eta` field.
- `cancellable` is true while the task can still be stopped. The archive requires cancel on a long task. It does not define this boolean.

### Pagination

```json
{"items": [], "next_cursor": null, "has_more": false}
```

Cursor pagination is a derived choice. The archive only said to decide before writing. `has_more: true` requires a `next_cursor`.

### Filters, timezone, locale

Not specified in the archive. A derived adapter may:

- Put filters in snake-case query fields, one field per constraint.
- Store instants as ISO-8601 strings with an offset, and keep a separate zone name if the interface must show local time. Do not call that format a sourced token.
- Keep locale selection on the client. If a file export must format a value, record the locale used. Do not translate the error `message`.

### Retry

The archive gives no retry count. Do not invent one and call it a token. A derived adapter may retry an operation only when that operation is marked idempotent, and the last failure still returns the stable `code`.

### Privacy, retention, audit

Sourced: minimize what is stored, keep product statistics visible and clearable by the person, and keep keys out of the UI.

Derived, because the archive has no audit schema and no retention period:

- An adapter does not log secrets, tokens, or key material.
- A retention job does not delete or keep data for an unstated number of days. If the product needs a period, it is a product decision and it is labeled as one.
- If an audit record is kept, the person can see it and clear it, the same way the archive treats statistics. It is not a hidden analytics stream.

## Adapters

Map every transport onto the same code enum.

| Transport in the archive | Reusable duty |
|---|---|
| Rust IPC `Result` | Stable code, no panic across the boundary |
| Optional Python JSON lines | Start failure, version mismatch, and crash each have a code and a degraded feature, not a dead app |
| Any later HTTP or queue boundary | Same codes, same progress rules, same refusal to send user copy |

Do not add a gateway, a hosted queue, or a paid API to satisfy this file.
