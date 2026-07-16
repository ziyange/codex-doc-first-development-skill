# Templates

Use these templates when the active task needs concrete docs or engineering artifacts. Keep empty sections out of final project docs unless they clarify expected future content.

## Contents

- [Directory Structures](#directory-structures)
- [Core Project Documents](#agentsmd)
- [Phase and Task Packs](#docsdeliveryphase-001md)
- [Coordination and Verification](#locksyml)
- [PR, Writeback, and Archive](#pr-body)

## Directory Structures

Quick mode:

```text
AGENTS.md
docs/
  README.md
  requirements.md
  delivery/
    TASK-001.md
```

Standard mode:

```text
AGENTS.md
docs/
  README.md
  product.md
  requirements.md
  architecture.md
  delivery/
    roadmap.md
    phase-001.md
    tasks/
      TASK-001.md
  verification/
    test-strategy.md
    reports/
  archive/
```

Strict mode:

```text
AGENTS.md
docs/
  README.md
  product.md
  requirements.md
  architecture.md
  decisions/
  delivery/
    roadmap.md
    phase-001.md
    tasks/
      TASK-001.md
    locks.yml
  verification/
    test-strategy.md
    quality-gate.md
    reports/
  archive/
```

Add `api.md`, `data-model.md`, `security.md`, `ux.md`, `operations.md`, or an ADR only when the project has applicable facts to record. Do not create placeholder-only optional documents.

## AGENTS.md

```markdown
# AGENTS.md

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
```

## docs/README.md

```markdown
# Docs Index

## Current Status

## Active Phase

## Source of Truth

## Key Documents

## Current Tasks

## Verification

## Archive
```

## docs/product.md

```markdown
# Product Brief

## Problem

## Target Users

## Core Scenarios

## MVP Scope

## Non-goals

## Success Criteria

## Constraints

## Assumptions

## Open Questions
```

## docs/requirements.md

```markdown
# Requirements

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
```

## docs/architecture.md

```markdown
# Architecture

## System Context

## Module Boundaries

## Data Flow

## Interface Contracts

## State Model

## Security and Permissions

## Operational Notes

## Known Constraints
```

## docs/delivery/phase-001.md

```markdown
# Phase 001: <phase name>

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
docs/archive/phase-001/
```

## Task Pack

```markdown
# TASK-001: <task name>

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
```

## locks.yml

Use only when multiple agents or branches may write overlapping areas.

```yaml
locks:
  - path: src/auth/**
    owner: TASK-001
    expires_at: <ISO-8601 timestamp>
    reason: auth implementation
```

## Verification Report

```markdown
# Verification Report

## Commit / Branch

## Evidence Source
- planned / local execution / isolated execution / external CI

## Commands

## Results

## Failed Tests

## Warnings

## Coverage

## Artifacts

## Conclusion
```

## PR Body

```markdown
## Summary

## Requirements

## Changes

## Tests

## Risks

## Screenshots / Artifacts

## Docs Updated
```

## Conflict Resolution Task

```markdown
# Conflict Resolution Task

## Conflict Source
- Task:
- Branch:
- Target Branch:
- Files:

## Conflict Type
- Text conflict
- Logic conflict
- Type conflict
- Interface conflict
- Test conflict
- Docs conflict

## Context
- Task Pack:
- Requirements:
- Architecture:
- Tests:

## Resolution Rules
1. Do not delete valid business logic from either side.
2. Do not change interface contracts without authorization.
3. Do not change data structures without authorization.
4. Do not delete relevant tests.
5. Re-run tests after resolving.

## Output
- Conflict cause:
- Resolution:
- Changed files:
- Test results:
- Continue merge:
```

## Writeback Patch

```yaml
patch_id: ""
change_id: ""
task_id: ""
requirement_ids:
  - ""
target_document: ""
operation: "add_section | update_section | append_item | replace_item | delete_item | update_table_row | add_table_row"
target_anchor: ""
content:
  title: ""
  body: ""
validation:
  required_fields:
    - ""
  must_update_index: true
  must_archive: true
```

## Phase Archive Summary

```markdown
# Phase 001 Summary

## Goal

## Completed

## Not Completed

## Requirements Status

## Major Changes

## Test Evidence

## Decisions

## Risks

## Next Phase Recommendations
```
