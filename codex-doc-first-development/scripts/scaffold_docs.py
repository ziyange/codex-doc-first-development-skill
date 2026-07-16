#!/usr/bin/env python3
"""Scaffold Codex document-first project docs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


AGENTS = """# AGENTS.md

## Project Commands
- Install:
- Dev:
- Test:
- Lint:
- Typecheck:
- Build:

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

    add("AGENTS.md", AGENTS)
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
        )
    except ValueError as exc:
        parser.error(str(exc))
    for path in written:
        print(path)
    label = "planned" if args.dry_run else "created_or_updated"
    print(f"{label}={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

