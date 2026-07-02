#!/usr/bin/env python3
"""Scaffold Codex document-first project docs."""

from __future__ import annotations

import argparse
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
- TASK-001:

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

## Context Pack

### Must Read
- docs/requirements.md#REQ-001
- docs/architecture.md

### Allowed Files
- src/...
- tests/...

### Forbidden Files
- ...

### Interfaces / Contracts

### Data Constraints

### UI Constraints

## Implementation Requirements

## Test Requirements

## Acceptance Criteria

## Done Definition

## Risks

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


def write_if_missing(path: Path, content: str, overwrite: bool) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def scaffold(root: Path, mode: str, phase: str, overwrite: bool) -> list[Path]:
    written: list[Path] = []

    def add(relative: str, content: str) -> None:
        path = root / relative
        if write_if_missing(path, content, overwrite):
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
        (root / "docs/verification/reports").mkdir(parents=True, exist_ok=True)
        (root / "docs/archive").mkdir(parents=True, exist_ok=True)

    if mode == "strict":
        add("docs/decisions/ADR-0001-example.md", "# ADR-0001: <decision title>\n\n## Status\nproposed\n\n## Context\n\n## Decision\n\n## Consequences\n")
        add("docs/api.md", "# API\n")
        add("docs/data-model.md", "# Data Model\n")
        add("docs/security.md", "# Security\n")
        add("docs/ux.md", "# UX\n")
        add("docs/operations.md", "# Operations\n")
        add("docs/delivery/locks.yml", LOCKS)
        add("docs/verification/quality-gate.md", QUALITY_GATE)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold Codex doc-first project docs.")
    parser.add_argument("--root", required=True, help="Project root where docs should be created.")
    parser.add_argument("--mode", choices=["quick", "standard", "strict"], default="standard")
    parser.add_argument("--phase", default="001", help="Phase number, e.g. 001.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    written = scaffold(root, args.mode, args.phase, args.overwrite)
    for path in written:
        print(path)
    print(f"created_or_updated={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

