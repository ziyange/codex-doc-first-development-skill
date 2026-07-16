#!/usr/bin/env python3
"""Check whether a Codex doc-first Task Pack is ready for execution."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "Status",
    "Requirement IDs",
    "Objective",
    "Context Pack",
    "Must Read",
    "Allowed Files",
    "Forbidden Files",
    "Interfaces / Contracts",
    "Data Constraints",
    "UI Constraints",
    "Implementation Requirements",
    "Test Requirements",
    "Acceptance Criteria",
    "Done Definition",
    "Risks",
    "Output Required",
]

CONTENT_REQUIRED_HEADINGS = [
    heading for heading in REQUIRED_HEADINGS if heading != "Context Pack"
]

HEADING_PATTERN = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)
PLACEHOLDER_PATTERNS = [
    re.compile(r"<[^>\n]+>"),
    re.compile(r"\.{3,}"),
    re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE),
]


def heading_matches(text: str, heading: str) -> list[re.Match[str]]:
    return [
        match
        for match in HEADING_PATTERN.finditer(text)
        if match.group("title").strip() == heading
    ]


def section_content(text: str, heading: str) -> str | None:
    matches = heading_matches(text, heading)
    if not matches:
        return None

    match = matches[0]
    level = len(match.group("marks"))
    end = len(text)
    for following in HEADING_PATTERN.finditer(text, match.end()):
        if len(following.group("marks")) <= level:
            end = following.start()
            break
    return text[match.end() : end].strip()


def looks_like_placeholder(content: str) -> bool:
    normalized = re.sub(r"(?m)^\s*(?:[-*+]|\d+\.)\s*", "", content).strip()
    if not normalized:
        return True
    return any(pattern.search(normalized) for pattern in PLACEHOLDER_PATTERNS)


def check_task_pack(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    title = re.search(r"^#\s+(TASK-\d{3,}):\s*(\S.*?)\s*$", text, re.MULTILINE)
    if not title:
        issues.append("missing top-level '# TASK-###: title'")
        title_id = None
    else:
        title_id = title.group(1)
        if looks_like_placeholder(title.group(2)):
            issues.append("top-level TASK-* title still looks like a placeholder")

    filename_id = re.fullmatch(r"(TASK-\d{3,})\.md", path.name, re.IGNORECASE)
    if title_id and filename_id and title_id.upper() != filename_id.group(1).upper():
        issues.append(
            f"title ID {title_id} does not match filename ID {filename_id.group(1)}"
        )

    for heading in REQUIRED_HEADINGS:
        matches = heading_matches(text, heading)
        if not matches:
            issues.append(f"missing heading: {heading}")
        elif len(matches) > 1:
            issues.append(f"duplicate heading: {heading}")

    requirement_ids = section_content(text, "Requirement IDs")
    if requirement_ids is not None and not re.search(r"\bREQ-\d{3,}\b", requirement_ids):
        issues.append("Requirement IDs must contain at least one REQ-### reference")

    for heading in CONTENT_REQUIRED_HEADINGS:
        content = section_content(text, heading)
        if content is not None and looks_like_placeholder(content):
            issues.append(f"section is empty or still contains placeholders: {heading}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a Codex doc-first Task Pack is ready for execution."
    )
    parser.add_argument("task_pack", help="Path to TASK-*.md")
    args = parser.parse_args()

    path = Path(args.task_pack)
    if not path.is_file():
        print(f"Task Pack check failed:\n- file not found: {path}", file=sys.stderr)
        return 2

    try:
        issues = check_task_pack(path)
    except (OSError, UnicodeError) as exc:
        print(f"Task Pack check failed:\n- cannot read {path}: {exc}", file=sys.stderr)
        return 2
    if issues:
        print("Task Pack check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Task Pack check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

