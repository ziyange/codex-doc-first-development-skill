#!/usr/bin/env python3
"""Check basic completeness of a Codex doc-first Task Pack."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_HEADINGS = [
    "Status",
    "Requirement IDs",
    "Objective",
    "Context Pack",
    "Must Read",
    "Allowed Files",
    "Forbidden Files",
    "Implementation Requirements",
    "Test Requirements",
    "Acceptance Criteria",
    "Done Definition",
    "Risks",
    "Output Required",
]


def heading_present(text: str, heading: str) -> bool:
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$", re.MULTILINE)
    return bool(pattern.search(text))


def check_task_pack(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    if not re.search(r"^#\s+TASK-\d{3,}:", text, re.MULTILINE):
        issues.append("missing top-level TASK-* title")

    if not re.search(r"\bREQ-\d{3,}\b", text):
        issues.append("missing REQ-* reference")

    for heading in REQUIRED_HEADINGS:
        if not heading_present(text, heading):
            issues.append(f"missing heading: {heading}")

    allowed = re.search(r"#+\s+Allowed Files\s*(.*?)(?:\n#+\s+|\Z)", text, re.DOTALL)
    if allowed and "..." in allowed.group(1) and len(allowed.group(1).strip()) < 20:
        issues.append("Allowed Files still looks like a placeholder")

    forbidden = re.search(r"#+\s+Forbidden Files\s*(.*?)(?:\n#+\s+|\Z)", text, re.DOTALL)
    if forbidden and "..." in forbidden.group(1) and len(forbidden.group(1).strip()) < 20:
        issues.append("Forbidden Files still looks like a placeholder")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Codex doc-first Task Pack.")
    parser.add_argument("task_pack", help="Path to TASK-*.md")
    args = parser.parse_args()

    path = Path(args.task_pack)
    issues = check_task_pack(path)
    if issues:
        print("Task Pack check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Task Pack check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

