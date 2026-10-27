#!/usr/bin/env python3
"""Prepare directory-distributed skill releases from the repository's changesets."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re

PACKAGE = "codex-doc-first-development-skill"
BUMP_ORDER = {"patch": 0, "minor": 1, "major": 2}


def read_changesets(root: Path) -> list[tuple[Path, str, str]]:
    folder = root / ".changeset"
    if not folder.is_dir():
        raise ValueError("missing .changeset directory")
    changes = []
    for path in sorted(folder.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        match = re.fullmatch(
            r'---\s*\n["\']?' + re.escape(PACKAGE)
            + r'["\']?:\s*(patch|minor|major)\s*\n---\s*\n(.*)',
            text, re.DOTALL,
        )
        if not match or not match[2].strip():
            raise ValueError(f"invalid changeset: {path.name}")
        changes.append((path, match[1], match[2].strip()))
    return changes


def prepare(root: Path) -> tuple[dict, dict[Path, str], list[Path]]:
    metadata_path = root / "pyproject.toml"
    metadata = metadata_path.read_text(encoding="utf-8")
    project = re.search(r"(?ms)^\[project\]\s*\n(.*?)(?=^\[|\Z)", metadata)
    if not project or not re.search(r'^name\s*=\s*"' + PACKAGE + r'"\s*$', project[1], re.MULTILINE):
        raise ValueError("pyproject.toml project name missing or unsupported")
    version = re.search(r'^version\s*=\s*"(\d+\.\d+\.\d+)"\s*$', project[1], re.MULTILINE)
    if not version:
        raise ValueError("project version must be a stable major.minor.patch")
    current = version[1]
    changes = read_changesets(root)
    result = {"status": "unchanged", "pending": bool(changes), "current_version": current,
              "next_version": current, "changesets": [path.name for path, _, _ in changes]}
    if not changes:
        return result, {}, []

    bump = max((kind for _, kind, _ in changes), key=BUMP_ORDER.get)
    major, minor, patch = map(int, current.split("."))
    next_version = {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0",
                    "patch": f"{major}.{minor}.{patch + 1}"}[bump]
    result.update(status="planned", next_version=next_version, bump=bump)
    start = project.start(1) + version.start(1)
    end = project.start(1) + version.end(1)
    updates = {metadata_path: metadata[:start] + next_version + metadata[end:]}

    # Validate every source before writing anything or consuming a changeset.
    for relative in ("codex-doc-first-development/SKILL.md", "README.md"):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        heading = re.search(r"(?m)^# .+$", text)
        if not heading or not re.search(r"\bv" + re.escape(current) + r"\b", heading[0]):
            raise ValueError(f"version drift in {relative}: expected v{current} in title")
        updates[path] = re.sub(r"\bv" + re.escape(current) + r"\b", "v" + next_version, text)

    changelog_path = root / "CHANGELOG.md"
    history = changelog_path.read_text(encoding="utf-8")
    first_entry = re.search(r"(?m)^## \[", history)
    if not first_entry:
        raise ValueError("CHANGELOG.md has no release entry")
    entry = f"## [{next_version}] - {date.today().isoformat()}\n\n### Changed\n\n"
    entry += "\n\n".join("- " + summary.replace("\n", "\n  ") for _, _, summary in changes) + "\n\n"
    updates[changelog_path] = history[:first_entry.start()] + entry + history[first_entry.start():]
    return result, updates, [path for path, _, _ in changes]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--apply", action="store_true", help="Write version changes and consume processed changesets")
    parser.add_argument("--json", action="store_true", help="Emit a structured release plan")
    args = parser.parse_args()
    try:
        result, updates, consumed = prepare(args.root.resolve())
        if args.apply and updates:
            for path, content in updates.items():
                path.write_text(content, encoding="utf-8")
            for path in consumed:
                path.unlink()
            result["status"] = "applied"
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"status": "error", "error": str(exc)}
        print(json.dumps(result) if args.json else str(exc))
        return 2
    print(json.dumps(result, indent=2) if args.json else f"{result['status']}: {result['next_version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
