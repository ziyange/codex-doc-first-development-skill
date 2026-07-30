#!/usr/bin/env python3
"""Check whether a Codex doc-first Task Pack is ready for execution."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


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

DUMMY_TEST_PATTERNS = [
    (re.compile(r"\bassert\s+True\b"), "Tautological 'assert True' detected"),
    (re.compile(r"\bassert\s+1\s*==\s*1\b"), "Tautological 'assert 1 == 1' detected"),
    (re.compile(r"\bself\.assertTrue\(\s*True\s*\)"), "Tautological 'assertTrue(True)' detected"),
    (re.compile(r"#\s*(?:self\.)?assert\b"), "Commented out assertion detected"),
    (re.compile(r"def\s+test_\w+\([^)]*\):\s*(?:pass|\.\.\.)\s*(?:\n|$)"), "Empty pass/ellipsis test body detected"),
]


def detect_dummy_test_patterns(text: str) -> List[str]:
    """
    Detects fake or dummy test patterns in code or task specification blocks.
    Returns list of warning descriptions.
    """
    findings = []
    for pattern, desc in DUMMY_TEST_PATTERNS:
        if pattern.search(text):
            findings.append(desc)
    return findings


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


def calculate_card_confidence(card_rules: Dict, context_text: str) -> float:
    """
    Calculates weighted confidence score:
    S = (2.0 * mandatory_hits + 1.0 * pattern_hits) / (2.0 * mandatory_total + 1.0 * pattern_total)
    Uses binary (0 or 1) feature hits per rule item.
    """
    mandatory_keywords = card_rules.get("mandatory_keywords", [])
    pattern_contexts = card_rules.get("pattern_contexts", [])

    m_total = len(mandatory_keywords)
    p_total = len(pattern_contexts)

    denominator = 2.0 * m_total + 1.0 * p_total
    if denominator == 0:
        return 0.0

    lower_text = context_text.lower()

    m_hits = sum(1 for kw in mandatory_keywords if kw.lower() in lower_text)
    p_hits = sum(1 for ctx in pattern_contexts if ctx.lower() in lower_text)

    score = (2.0 * m_hits + 1.0 * p_hits) / denominator
    return min(1.0, max(0.0, score))


def check_task_pack(path: Path, schemas_md_path: Optional[Path] = None) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    warnings: list[str] = []

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

    allowed_files_content = section_content(text, "Allowed Files")
    if allowed_files_content is not None:
        lines = [line.strip() for line in allowed_files_content.splitlines() if line.strip()]
        for line in lines:
            item = re.sub(r"^(?:[-*+]|\d+\.)\s*", "", line).strip()
            if not item:
                continue
            if (
                item in {"*", "**", ".", "*.*", "./*", "./**", "**/*"}
                or re.fullmatch(r"^(?:\.|\*+|\./\*+|\*\*/\*+|(?:[a-zA-Z0-9_-]+)/\*+)$", item)
            ):
                issues.append(
                    f"Allowed Files is overly broad: '{item}' is forbidden without explicit narrow file patterns"
                )

    # v2.0.0 Governance Checks: MAX_ITERATIONS validation
    max_iter_match = re.search(r"MAX_ITERATIONS:\s*(\d+)", text)
    if max_iter_match:
        val = int(max_iter_match.group(1))
        if val < 1 or val > 10:
            issues.append(f"MAX_ITERATIONS value {val} must be an integer between 1 and 10")
    else:
        # Legacy v1.x task pack warning
        warnings.append("MAX_ITERATIONS heading missing (v1.x legacy format fallback active)")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a Codex doc-first Task Pack is ready for execution."
    )
    parser.add_argument("task_pack", help="Path to TASK-*.md")
    parser.add_argument("--json", action="store_true", help="Output results in structured JSON format")
    parser.add_argument("--schemas", default=None, help="Path to references/schemas.md for dynamic validation")
    args = parser.parse_args()

    path = Path(args.task_pack)
    if not path.is_file():
        if args.json:
            print(
                json.dumps(
                    {"status": "error", "file": str(path), "issues": [f"file not found: {path}"]},
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print(f"Task Pack check failed:\n- file not found: {path}", file=sys.stderr)
        return 2

    try:
        issues = check_task_pack(path, schemas_md_path=Path(args.schemas) if args.schemas else None)
    except (OSError, UnicodeError) as exc:
        if args.json:
            print(
                json.dumps(
                    {"status": "error", "file": str(path), "issues": [f"cannot read {path}: {exc}"]},
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print(f"Task Pack check failed:\n- cannot read {path}: {exc}", file=sys.stderr)
        return 2

    status = "failed" if issues else "passed"
    if args.json:
        print(
            json.dumps(
                {
                    "status": status,
                    "file": str(path),
                    "total_issues": len(issues),
                    "issues": issues,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        if issues:
            print("Task Pack check failed:")
            for issue in issues:
                print(f"- {issue}")
        else:
            print("Task Pack check passed.")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
