#!/usr/bin/env python3
"""Checks for the derived UX payloads in references/backend-contracts.md.

The archive requires stable error codes, client-owned sentences, measurable
progress, and cancel. It does not define these JSON shapes. This module
checks the derived shapes only.
"""

from __future__ import annotations

import re
import sys

SNAKE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
TOKEN = re.compile(r"^[a-z][a-z0-9_]*$")
USER_COPY_KEYS = {"user_message", "user_copy", "localized_message"}
ETA_KEYS = {"eta", "eta_seconds", "fake_eta"}
PROGRESS_STATES = {"queued", "running", "succeeded", "failed", "cancelled"}


def _walk_keys(value, path="$"):
    problems = []
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{path}.{key}"
            if not isinstance(key, str) or not SNAKE.fullmatch(key):
                problems.append(f"{here} is not snake_case")
            problems.extend(_walk_keys(child, here))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            problems.extend(_walk_keys(child, f"{path}[{index}]"))
    return problems


def error_problems(payload, allowed_codes) -> list[str]:
    problems = []
    if not isinstance(payload, dict):
        return ["error payload must be an object"]
    problems.extend(_walk_keys(payload))
    extra = USER_COPY_KEYS.intersection(payload)
    if extra:
        problems.append("server must not send user copy keys: " + ", ".join(sorted(extra)))
    code = payload.get("code")
    message = payload.get("message")
    if not isinstance(code, str) or code not in allowed_codes:
        problems.append("code must be one of the project enum")
    if not isinstance(message, str) or not TOKEN.fullmatch(message):
        problems.append("message must be a stable token, not a translated sentence")
    return problems


def progress_problems(payload) -> list[str]:
    problems = []
    if not isinstance(payload, dict):
        return ["progress payload must be an object"]
    problems.extend(_walk_keys(payload))
    if ETA_KEYS.intersection(payload):
        problems.append("progress must not carry an ETA")
    if not isinstance(payload.get("task_id"), str) or not payload["task_id"]:
        problems.append("task_id must be a non-empty string")
    if payload.get("state") not in PROGRESS_STATES:
        problems.append("state must be one of the derived progress states")
    if not isinstance(payload.get("cancellable"), bool):
        problems.append("cancellable must be a boolean")
    completed = payload.get("completed")
    total = payload.get("total")
    if "percent" in payload and total is None:
        problems.append("percent requires a measurable total")
    if total is not None:
        if not isinstance(completed, int) or not isinstance(total, int):
            problems.append("completed and total must be integers when total is known")
        elif completed < 0 or total < 0 or completed > total:
            problems.append("completed must sit inside 0..total")
    return problems


def page_problems(payload) -> list[str]:
    problems = []
    if not isinstance(payload, dict):
        return ["page payload must be an object"]
    problems.extend(_walk_keys(payload))
    if not isinstance(payload.get("items"), list):
        problems.append("items must be a list")
    if not isinstance(payload.get("has_more"), bool):
        problems.append("has_more must be a boolean")
    cursor = payload.get("next_cursor")
    if cursor is not None and not isinstance(cursor, str):
        problems.append("next_cursor must be a string or null")
    if payload.get("has_more") is True and not cursor:
        problems.append("has_more requires next_cursor")
    return problems


def main() -> int:
    codes = {"not_found", "invalid_input"}
    checks = [
        error_problems({"code": "not_found", "message": "not_found"}, codes) == [],
        error_problems({"code": "not_found", "message": "找不到", "user_message": "找不到"}, codes) != [],
        error_problems({"code": "nope", "message": "nope"}, codes) != [],
        progress_problems(
            {"task_id": "export_1", "state": "running", "completed": 1, "total": 4, "cancellable": True}
        )
        == [],
        progress_problems(
            {"task_id": "export_1", "state": "running", "completed": 1, "total": None, "percent": 10, "eta": 5, "cancellable": True}
        )
        != [],
        page_problems({"items": [], "next_cursor": None, "has_more": False}) == [],
        page_problems({"items": [], "next_cursor": None, "has_more": True}) != [],
        page_problems({"items": [], "nextCursor": None, "has_more": False}) != [],
    ]
    if not all(checks):
        print("ux_contract self-check failed")
        return 1
    print("ux_contract self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
