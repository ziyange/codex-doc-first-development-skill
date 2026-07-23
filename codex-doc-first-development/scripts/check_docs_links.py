#!/usr/bin/env python3
"""Check relative links and heading anchors in Markdown documentation files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

LINK_PATTERN = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)")
HEADING_PATTERN = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)


def heading_to_slugs(title: str) -> set[str]:
    """Generate potential anchor slugs for a heading title."""
    clean_title = re.sub(r"<[^>]+>", "", title).strip()
    slugs = set()

    # 1. Exact raw title
    slugs.add(clean_title.lower())

    # 2. GFM style slug
    gfm = re.sub(r"[^\w\s\-\u4e00-\u9fff]", "", clean_title.lower())
    gfm_slug = re.sub(r"[\s_]+", "-", gfm).strip("-")
    if gfm_slug:
        slugs.add(gfm_slug)

    # 3. Simple space-to-hyphen slug
    simple_slug = re.sub(r"\s+", "-", clean_title.lower())
    slugs.add(simple_slug)

    # 4. Strip dot numbering prefix like "6.1 " -> "61-" or "6.1-"
    normalized_dots = clean_title.lower().replace(".", "")
    gfm_nodots = re.sub(r"[^\w\s\-\u4e00-\u9fff]", "", normalized_dots)
    nodots_slug = re.sub(r"[\s_]+", "-", gfm_nodots).strip("-")
    if nodots_slug:
        slugs.add(nodots_slug)

    return slugs


def extract_doc_anchors(content: str) -> set[str]:
    """Extract all available heading anchors in a markdown document."""
    anchors = set()
    for match in HEADING_PATTERN.finditer(content):
        title = match.group("title")
        anchors.update(heading_to_slugs(title))
    return anchors


def find_line_number(content: str, index: int) -> int:
    """Find 1-based line number for a character index in content."""
    return content.count("\n", 0, index) + 1


def check_markdown_file(
    file_path: Path, root_path: Path, cache: dict[Path, set[str]]
) -> list[dict[str, str | int]]:
    """Check a single markdown file for broken relative links and anchors."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [
            {
                "file": str(file_path.relative_to(root_path)),
                "line": 1,
                "target": str(file_path),
                "reason": f"cannot read file: {exc}",
            }
        ]

    issues: list[dict[str, str | int]] = []
    rel_file_str = str(file_path.relative_to(root_path)) if file_path.is_relative_to(root_path) else str(file_path)

    for match in LINK_PATTERN.finditer(content):
        raw_target = match.group("target").strip()
        # Handle title attributes in links, e.g. [label](path "title")
        if " " in raw_target:
            raw_target = raw_target.split(" ", 1)[0]
        raw_target = raw_target.strip('"\'')

        # Skip external URLs or mailto
        if raw_target.startswith(("http://", "https://", "mailto:", "ftp://", "//", "javascript:")):
            continue

        line_num = find_line_number(content, match.start())
        parsed = urllib.parse.urlsplit(raw_target)
        path_part = parsed.path
        fragment_part = parsed.fragment

        # Case A: Same file anchor, e.g. #section-name
        if not path_part and fragment_part:
            if file_path not in cache:
                cache[file_path] = extract_doc_anchors(content)
            available_anchors = cache[file_path]
            target_slug = fragment_part.lower()
            if target_slug not in available_anchors:
                issues.append(
                    {
                        "file": rel_file_str,
                        "line": line_num,
                        "target": raw_target,
                        "reason": f"anchor '#{fragment_part}' not found in current document",
                    }
                )
            continue

        # Case B: File link (with or without anchor)
        target_path_str = urllib.parse.unquote(path_part)
        if target_path_str.startswith("file:///"):
            target_path_str = target_path_str[8:]

        target_file = (file_path.parent / target_path_str).resolve()

        if not target_file.exists():
            issues.append(
                {
                    "file": rel_file_str,
                    "line": line_num,
                    "target": raw_target,
                    "reason": f"linked target file does not exist: {target_path_str}",
                }
            )
            continue

        # If target file exists and has anchor, check anchor
        if fragment_part and target_file.is_file() and target_file.suffix.lower() == ".md":
            if target_file not in cache:
                try:
                    target_content = target_file.read_text(encoding="utf-8")
                    cache[target_file] = extract_doc_anchors(target_content)
                except (OSError, UnicodeError):
                    cache[target_file] = set()

            available_anchors = cache[target_file]
            target_slug = fragment_part.lower()
            if target_slug not in available_anchors:
                issues.append(
                    {
                        "file": rel_file_str,
                        "line": line_num,
                        "target": raw_target,
                        "reason": f"anchor '#{fragment_part}' not found in target file '{target_path_str}'",
                    }
                )

    return issues


def check_docs_links(root: Path) -> dict[str, object]:
    """Scan all markdown files under root and return verification results."""
    root = root.resolve()
    if not root.exists():
        return {
            "status": "error",
            "message": f"path not found: {root}",
            "total_files": 0,
            "total_issues": 1,
            "issues": [{"file": str(root), "line": 1, "target": str(root), "reason": "path not found"}],
        }

    md_files: list[Path] = []
    if root.is_file():
        if root.suffix.lower() == ".md":
            md_files.append(root)
        search_root = root.parent
    else:
        search_root = root
        for path in sorted(root.rglob("*.md")):
            if any(part.startswith(".") or part in {"node_modules", "venv", "target", "build", "dist"} for part in path.parts):
                continue
            md_files.append(path)

    cache: dict[Path, set[str]] = {}
    all_issues: list[dict[str, str | int]] = []

    for file_path in md_files:
        issues = check_markdown_file(file_path, search_root, cache)
        all_issues.extend(issues)

    status = "passed" if not all_issues else "failed"
    return {
        "status": status,
        "total_files": len(md_files),
        "total_issues": len(all_issues),
        "issues": all_issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check relative links and heading anchors in Markdown docs."
    )
    parser.add_argument("path", nargs="?", default=".", help="Project root or specific Markdown file/directory")
    parser.add_argument("--json", action="store_true", help="Output results in structured JSON format")
    args = parser.parse_args()

    target_path = Path(args.path)
    result = check_docs_links(target_path)

    if result.get("status") == "error":
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Link check error: {result.get('message')}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["total_issues"] == 0:
            print(f"Docs link check passed ({result['total_files']} markdown files checked).")
        else:
            print(f"Docs link check failed ({result['total_issues']} broken links found in {result['total_files']} files):")
            for issue in result["issues"]:
                print(f"- {issue['file']}:{issue['line']} -> {issue['target']} ({issue['reason']})")

    return 0 if result["total_issues"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
