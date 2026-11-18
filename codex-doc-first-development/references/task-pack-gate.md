# Task Pack Gate Reference

Distilled from the Task Pack Gate and Test Quality & DRY Reusability Gate in the doc-first lifecycle. Use with the main `codex-doc-first-development` orchestrator; this file is the detail behind its S9-S10 delegation steps.

This reference applies only when a [formal Task Pack](task-pack.md) is required.
Structural readiness is separate from user authorization, dependency readiness,
tests, and runtime acceptance.

## Required sections (16)

Status, Requirement IDs, Objective, Context Pack, Must Read, Allowed Files, Forbidden Files, Interfaces / Contracts, Data Constraints, UI Constraints, Implementation Requirements, Test Requirements, Acceptance Criteria, Done Definition, Risks, Output Required.

## What the CLI enforces (blocking `issues`)

| Check | Rule |
|---|---|
| Title | `# TASK-###: <title>` present; title ID matches filename ID |
| Headings | all 16 present, each exactly once (duplicates rejected) |
| Requirement IDs | at least one `REQ-\d{3,}` in the Requirement IDs section |
| Placeholders | no `<...>`, `...`, `TODO`, `TBD` in required sections; Context Pack exempt |
| Allowed Files | no broad wildcards: `*`, `**`, `.`, `*.*`, `./*`, `**/*`, or `<dir>/*` shapes |
| MAX_ITERATIONS | when numeric value present, 1 <= N <= 10; missing legacy values warn; Goal execution requires an explicit valid limit |

## What the CLI surfaces (non-blocking `warnings`)

- `MAX_ITERATIONS heading missing (v1.x legacy format fallback active)`
- Tautological test patterns inside Test Requirements: `assert True`, `assert 1 == 1`, `assertTrue(True)`, commented-out assertions, empty `pass`/`...` test bodies

Warnings never change the exit code. Consider relevant warnings in the single delivery review.

## Test Quality & DRY Reusability Gate (S14)

See [delivery review criteria](review-gates.md#before-delivering).
