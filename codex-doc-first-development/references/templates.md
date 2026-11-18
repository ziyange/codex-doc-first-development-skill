# Templates

Use these templates when the active task needs concrete docs or engineering artifacts. Keep empty sections out of final project docs unless they clarify expected future content.
Apply [Adaptive Workflow](adaptive-workflow.md) first. Reuse existing records and paths. Directory layouts below document the explicit scaffolder; they are not required artifacts for a risk tier.

## Contents

- [Directory Structures](#directory-structures)
- [Core Project Documents](#agentsmd)
- [Plan Point Record](#plan-point-record)
- [Pain-Point Card Template](#pain-point-card-template)
- [Phase and Task Packs](#docsdeliveryphase-001md)
- [Coordination Locks](#locksyml)
- [Handoff](#handoff)

## Directory Structures

Quick initialization layout (only when explicitly requested):

```text
AGENTS.md
docs/
  README.md
  requirements.md
  delivery/
    TASK-001.md
```

Explicit standard scaffold:

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

Explicit strict scaffold:

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

## Plan Point Record

Reuse a task or plan entry where available. Fill this same entry before and
after work. For Quick work with no record, state the scope and planned check
at intake and give the result in the final reply.

| Plan point | Allowed scope | Observable acceptance | Planned check | Actual result and evidence |
|---|---|---|---|---|
| Export preserves filtered rows | Export code, behavior tests, owning contract | CSV matches the current filter | Run export tests | Pending until verified |

For a required formal Task Pack, use its own status and evidence. For the
opt-in transaction format, see [runtime audit](runtime-audit.md).

## Pain-Point Card Template

```json
{
  "card_id": "CARD_NAME",
  "title": "Card Descriptive Title",
  "category": "CONCURRENCY_RACE",
  "trigger_rules": {
    "mandatory_keywords": ["keyword1", "keyword2"],
    "pattern_contexts": ["context1", "context2"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

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

## Unified Service Layer & DRY API Design

## Data Flow & Backend Field Projection

## Interface Contracts

## State Model

## Security and Permissions

## Operational Notes

## Known Constraints
```

## docs/ux.md

```markdown
# UX & UI Design

## Applicability

## Product Prototype & Navigation Flow

## Screen UI Layouts & Visual Mockups
<!-- Embed generated UI preview images here if multimodal/generate_image is available: ![Screen Preview](path/to/image.png) -->

## UI Component to API Interface Binding Table
| Screen / Component | User Action | Unified API Module / Route | Request Parameters | Projected Fields | UI State (Loading/Empty/Error) |
|---|---|---|---|---|---|
| ExampleScreen / SubmitBtn | Click Submit | ApiClient.submitData() | `{ id: 123 }` | `status, result` | Button spinner, inline error toast |

## User Interaction & State Transitions
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

Use this template only when a formal pack is required. Add the actual check
and outcome to this same record and update its status.

## locks.yml

Use only when multiple agents or branches may write overlapping areas.

```yaml
locks:
  - path: src/auth/**
    owner: TASK-001
    expires_at: <ISO-8601 timestamp>
    reason: auth implementation
```

## Handoff

For a PR or an archive that the project needs, summarize the outcome and link
the authoritative task entries, existing check results, and material risks.
Keep conflict resolutions and verification outcomes in the original record.
Write independent product or engineering facts into the owning docs.

## Structured JSON Contracts & Schema

Use these JSON Schemas to validate machine-readable CLI outputs and CI/CD contract payloads.

### Check Results Schema (bundled check_task_pack.py & check_docs_links.py)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CheckResult",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["passed", "failed", "error"]
    },
    "file": { "type": "string" },
    "total_files": { "type": "integer" },
    "total_issues": { "type": "integer" },
    "issues": {
      "type": "array",
      "items": {
        "oneOf": [
          { "type": "string" },
          {
            "type": "object",
            "properties": {
              "file": { "type": "string" },
              "line": { "type": "integer" },
              "target": { "type": "string" },
              "reason": { "type": "string" }
            },
            "required": ["file", "line", "target", "reason"]
          }
        ]
      }
    }
  },
  "required": ["status", "issues"]
}
```

### Scaffold Summary Schema (scaffold_docs.py --json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ScaffoldSummary",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["created_or_updated", "planned"]
    },
    "mode": {
      "type": "string",
      "enum": ["quick", "standard", "strict"]
    },
    "phase": { "type": "string" },
    "root": { "type": "string" },
    "files": {
      "type": "array",
      "items": { "type": "string" }
    },
    "count": { "type": "integer" }
  },
  "required": ["status", "mode", "phase", "files", "count"]
}
```
