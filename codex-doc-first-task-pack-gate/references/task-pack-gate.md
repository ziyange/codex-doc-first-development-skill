# Task Pack Gate Reference

Distilled from the Task Pack Gate and Test Quality & DRY Reusability Gate in the doc-first lifecycle. Use with the main `codex-doc-first-development` orchestrator; this file is the detail behind its S9-S10 delegation steps.

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
| MAX_ITERATIONS | integer, 1 <= N <= 10 |

## What the CLI surfaces (non-blocking `warnings`)

- `MAX_ITERATIONS heading missing (v1.x legacy format fallback active)`
- Tautological test patterns inside Test Requirements: `assert True`, `assert 1 == 1`, `assertTrue(True)`, commented-out assertions, empty `pass`/`...` test bodies

Warnings never change the exit code; they route to the S14 test-quality review.

## Test Quality & DRY Reusability Gate (S14)

Good tests and implementations:

- cover acceptance criteria
- assert behavior, state, output, or side effects
- include failure paths, edge cases, and boundary conditions for modified logic
- avoid mocking the core behavior under test
- reuse the centralized data client / service modules (no duplicated API call logic)
- run reliably in local or CI environments

Rejected anti-patterns:

- empty test functions or tests without assertions (`def test_foo(): pass`)
- `assert True`, `assertTrue(True)`, `expect(true).toBe(true)`
- HTTP status-only checks (200 without payload/state/contract assertions)
- truthiness-only assertions where exact values matter
- mocks replacing the unit under test instead of its dependencies
- missing boundary, permission, or error-path coverage for changed logic
- duplicate network request boilerplate instead of the centralized service module
