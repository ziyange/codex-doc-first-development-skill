#!/usr/bin/env python3
"""Scaffold Codex document-first project docs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


AGENTS_TEMPLATE = """# AGENTS.md

## Project Commands
- Install:{install}
- Dev:{dev}
- Test:{test}
- Lint:{lint}
- Typecheck:{typecheck}
- Build:{build}

## Coding Rules

## Testing Rules

## Git Rules

## Documentation Rules

## Agent Collaboration Rules
- Follow platform, user, and repository instructions before generated project guidance.
- Do not create subagents unless the user has explicitly authorized them.

## Forbidden Actions

"""

DOCS_INDEX = """# Docs Index

## Current Status

## Active Phase

## Source of Truth

## Key Documents

## Current Tasks

## Verification

## Archive
"""

PRODUCT = """# Product Brief

## Problem

## Target Users

## Core Scenarios

## MVP Scope

## Non-goals

## Success Criteria

## Constraints

## Assumptions

## Open Questions
"""

REQUIREMENTS = """# Requirements

## REQ-001: <requirement name>

User story:
As a <user>, I want <capability>, so that <value>.

Scope:
- Includes:
- Excludes:

Acceptance criteria:
- AC-001:
- AC-002:

Verification:
- Unit test:
- Integration test:
- UI verification:
- Manual acceptance:

Status: proposed
Priority:
Risk:
Dependencies:
"""

ARCHITECTURE = """# Architecture

## System Context

## Module Boundaries

## Data Flow

## Interface Contracts

## State Model

## Security and Permissions

## Operational Notes

## Known Constraints
"""

ROADMAP = """# Roadmap

## Phase 001
- Goal:
- Status: planned
"""

PHASE = """# Phase {phase}: <phase name>

## Goal

## Scope

## Non-goals

## Requirements
- REQ-001:

## Tasks
| Task ID | Objective | Requirements | Depends On | Parallel | Status |
|---|---|---|---|---|---|
| TASK-001 | | REQ-001 | none | no | planned |

## Dependencies

## Branch Strategy

## Agent Strategy

## Test Strategy

## Acceptance Gate

## Risks

## Archive Path
docs/archive/phase-{phase}/
"""

TASK = """# TASK-001: <task name>

## Status
planned

## Requirement IDs
- REQ-001

## Objective
<state one verifiable outcome>

## Context Pack

### Must Read
- docs/requirements.md#REQ-001
- docs/architecture.md

### Allowed Files
- <path or glob>

### Forbidden Files
- None outside Allowed Files.

### Interfaces / Contracts
- Not applicable: <explain why, or replace with contract details>.

### Data Constraints
- Not applicable: <explain why, or replace with data constraints>.

### UI Constraints
- Not applicable: <explain why, or replace with UI constraints>.

## Implementation Requirements
- <required behavior and boundaries>

## Test Requirements
- <command and expected behavior>

## Acceptance Criteria
- <observable result>

## Done Definition
- Acceptance criteria are met and required checks pass.

## Risks
- None identified.

## Output Required
- Changed files
- Test commands and results
- Notes and risks
"""

TEST_STRATEGY = """# Test Strategy

## Verification Levels
- L1 targeted local verification:
- L2 local lint/test/typecheck/build:
- L3 clean environment or sandbox:
- L4 CI / PR checks:

## Required Commands

## Quality Gate

## Skipped Checks Policy
"""

QUALITY_GATE = """# Quality Gate

## Test Quality

## Acceptance Evidence

## Merge Gate

## Blocked Conditions
"""

LOCKS = """locks: []
"""

API = """# API

## Applicability

## Contracts

## Errors and Compatibility
"""

DATA_MODEL = """# Data Model

## Applicability

## Entities and Relationships

## State and Migration Constraints
"""

SECURITY = """# Security

## Applicability

## Trust Boundaries and Permissions

## Threats, Secrets, and Audit Requirements
"""

UX = """# UX

## Applicability

## User Flows and States

## Accessibility and Visual Verification
"""

OPERATIONS = """# Operations

## Applicability

## Deployment and Rollback

## Monitoring and Incident Response
"""

OPTIONAL_STRICT_DOCS = {
    "api": ("docs/api.md", API),
    "data-model": ("docs/data-model.md", DATA_MODEL),
    "security": ("docs/security.md", SECURITY),
    "ux": ("docs/ux.md", UX),
    "operations": ("docs/operations.md", OPERATIONS),
}


def detect_stack(root: Path) -> dict[str, str]:
    """Detect project stack and return default commands for single or Monorepo projects."""
    commands = {
        "install": "",
        "dev": "",
        "test": "",
        "lint": "",
        "typecheck": "",
        "build": "",
    }

    # Collect paths to check: root first, then 1st & 2nd level subdirectories (e.g. packages/*, services/*)
    search_dirs = [root]
    if root.exists() and root.is_dir():
        for child in sorted(root.iterdir()):
            if (
                child.is_dir()
                and not child.name.startswith(".")
                and child.name not in {"node_modules", "venv", "env", "target", "build", "dist", "vendor", "docs", "tests", "archive"}
            ):
                search_dirs.append(child)
                try:
                    for grandchild in sorted(child.iterdir()):
                        if (
                            grandchild.is_dir()
                            and not grandchild.name.startswith(".")
                            and grandchild.name not in {"node_modules", "venv", "env", "target", "build", "dist", "vendor"}
                        ):
                            search_dirs.append(grandchild)
                except OSError:
                    pass

    # 1. Monorepo / Workspace level detectors at root
    if (root / "pnpm-workspace.yaml").exists():
        commands["install"] = "pnpm install"
        commands["dev"] = "pnpm dev"
        commands["test"] = "pnpm -r test"
        commands["build"] = "pnpm -r build"
        return commands

    if (root / "go.work").exists():
        commands["install"] = "go work sync"
        commands["test"] = "go test ./..."
        commands["build"] = "go build ./..."
        return commands

    if (root / "Cargo.toml").exists():
        cargo_content = ""
        try:
            cargo_content = (root / "Cargo.toml").read_text(encoding="utf-8")
        except OSError:
            pass
        if "[workspace]" in cargo_content:
            commands["install"] = "cargo build"
            commands["test"] = "cargo test --workspace"
            commands["lint"] = "cargo clippy"
            commands["build"] = "cargo build --release"
            return commands

    # 2. Iterate search_dirs for primary stack detection
    for d in search_dirs:
        # Makefile
        makefile = d / "Makefile"
        if makefile.exists() and not commands["test"]:
            try:
                content = makefile.read_text(encoding="utf-8")
                if re.search(r"^test\s*:", content, re.MULTILINE):
                    commands["test"] = "make test"
                if re.search(r"^build\s*:", content, re.MULTILINE):
                    commands["build"] = "make build"
                if re.search(r"^dev\s*:", content, re.MULTILINE):
                    commands["dev"] = "make dev"
                if re.search(r"^lint\s*:", content, re.MULTILINE):
                    commands["lint"] = "make lint"
            except OSError:
                pass

        # package.json
        if (d / "package.json").exists() and not commands["test"]:
            commands["install"] = commands["install"] or "npm install"
            commands["dev"] = commands["dev"] or "npm run dev"
            commands["test"] = commands["test"] or "npm test"
            commands["lint"] = commands["lint"] or "npm run lint"
            commands["build"] = commands["build"] or "npm run build"

        # Python
        if (
            (d / "pyproject.toml").exists()
            or (d / "requirements.txt").exists()
            or (d / "setup.py").exists()
        ) and not commands["test"]:
            commands["install"] = commands["install"] or "pip install -r requirements.txt"
            commands["test"] = commands["test"] or "pytest"
            commands["lint"] = commands["lint"] or "flake8"

        # Cargo.toml
        if (d / "Cargo.toml").exists() and not commands["test"]:
            commands["install"] = commands["install"] or "cargo build"
            commands["test"] = commands["test"] or "cargo test"
            commands["lint"] = commands["lint"] or "cargo clippy"
            commands["build"] = commands["build"] or "cargo build --release"

        # go.mod
        if (d / "go.mod").exists() and not commands["test"]:
            commands["install"] = commands["install"] or "go mod download"
            commands["test"] = commands["test"] or "go test ./..."
            commands["build"] = commands["build"] or "go build ./..."

        # CMakeLists.txt
        if (d / "CMakeLists.txt").exists() and not commands["build"]:
            commands["build"] = commands["build"] or "cmake -B build && cmake --build build"
            commands["test"] = commands["test"] or "ctest --test-dir build"

        # Dockerfile / docker-compose
        if (d / "docker-compose.yml").exists() or (d / "docker-compose.yaml").exists():
            if not commands["dev"]:
                commands["dev"] = "docker compose up"
        elif (d / "Dockerfile").exists():
            if not commands["build"]:
                commands["build"] = "docker build -t app ."

    return commands


def write_if_missing(
    path: Path, content: str, overwrite: bool, dry_run: bool = False
) -> bool:
    if path.exists() and not overwrite:
        return False
    if dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def scaffold(
    root: Path,
    mode: str,
    phase: str,
    overwrite: bool,
    include: tuple[str, ...] = (),
    dry_run: bool = False,
    auto_detect: bool = False,
) -> list[Path]:
    if not re.fullmatch(r"\d{3,}", phase):
        raise ValueError("phase must contain at least three digits, for example 001")
    if include and mode != "strict":
        raise ValueError("--include is only valid with --mode strict")

    written: list[Path] = []

    def add(relative: str, content: str) -> None:
        path = root / relative
        if write_if_missing(path, content, overwrite, dry_run):
            written.append(path)

    default_map = {"install": "", "dev": "", "test": "", "lint": "", "typecheck": "", "build": ""}
    if auto_detect:
        detected = detect_stack(root)
        default_map.update(detected)
    cmd_map = {k: f" {v}" if v else "" for k, v in default_map.items()}
    agents_content = AGENTS_TEMPLATE.format(**cmd_map)



    add("AGENTS.md", agents_content)
    add("docs/README.md", DOCS_INDEX)
    add("docs/requirements.md", REQUIREMENTS)
    add("docs/delivery/TASK-001.md" if mode == "quick" else "docs/delivery/tasks/TASK-001.md", TASK)

    if mode in {"standard", "strict"}:
        add("docs/product.md", PRODUCT)
        add("docs/architecture.md", ARCHITECTURE)
        add("docs/delivery/roadmap.md", ROADMAP)
        add(f"docs/delivery/phase-{phase}.md", PHASE.format(phase=phase))
        add("docs/verification/test-strategy.md", TEST_STRATEGY)
        if not dry_run:
            (root / "docs/verification/reports").mkdir(parents=True, exist_ok=True)
            (root / "docs/archive").mkdir(parents=True, exist_ok=True)

    if mode == "strict":
        add("docs/delivery/locks.yml", LOCKS)
        add("docs/verification/quality-gate.md", QUALITY_GATE)
        if not dry_run:
            (root / "docs/decisions").mkdir(parents=True, exist_ok=True)
        for name in dict.fromkeys(include):
            relative, content = OPTIONAL_STRICT_DOCS[name]
            add(relative, content)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Codex doc-first project docs.")
    parser.add_argument("--root", required=True, help="Project root where docs should be created.")
    parser.add_argument("--mode", choices=["quick", "standard", "strict"], default="standard")
    parser.add_argument(
        "--phase", default="001", help="Phase number with at least three digits, e.g. 001."
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing scaffold-managed files."
    )
    parser.add_argument(
        "--include",
        action="append",
        choices=sorted(OPTIONAL_STRICT_DOCS),
        default=[],
        help="Add an applicable optional strict-mode document; repeat as needed.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List files without creating or changing them."
    )
    parser.add_argument(
        "--auto-detect", action="store_true", help="Detect project stack and populate AGENTS.md commands."
    )
    parser.add_argument(
        "--json", action="store_true", help="Output scaffolding results in structured JSON format."
    )
    args = parser.parse_args()

    if args.include and args.mode != "strict":
        parser.error("--include is only valid with --mode strict")

    root = Path(args.root).resolve()
    try:
        written = scaffold(
            root,
            args.mode,
            args.phase,
            args.overwrite,
            tuple(args.include),
            args.dry_run,
            args.auto_detect,
        )
    except ValueError as exc:
        parser.error(str(exc))

    label = "planned" if args.dry_run else "created_or_updated"
    if args.json:
        rel_files = [str(p.relative_to(root)) if p.is_relative_to(root) else str(p) for p in written]
        output = {
            "status": label,
            "mode": args.mode,
            "phase": args.phase,
            "root": str(root),
            "files": rel_files,
            "count": len(written),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        for path in written:
            print(path)
        print(f"{label}={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
