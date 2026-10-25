---
name: codex-doc-first-task-pack-gate
description: Use when creating, reviewing, or validating a Task Pack (TASK-###.md) before agent code execution: required sections, explicit Allowed Files granularity, MAX_ITERATIONS bounds, contract anchors, tautological-test rejection, and placeholder detection.
---

# Task Pack Gate

A Task Pack (`TASK-###.md`) is the only artifact that authorizes code changes. This skill is the reusable discipline behind S9-S10 of the doc-first lifecycle: it makes a Task Pack executable before a single line of code is written.

## Readiness checklist

A Task Pack passes the gate only when all of the following hold:

- Title is `# TASK-###: <concrete title>`, and the ID matches the filename.
- All 16 required headings are present exactly once: Status, Requirement IDs, Objective, Context Pack, Must Read, Allowed Files, Forbidden Files, Interfaces / Contracts, Data Constraints, UI Constraints, Implementation Requirements, Test Requirements, Acceptance Criteria, Done Definition, Risks, Output Required.
- Requirement IDs contain at least one `REQ-###` reference.
- Every required section (except Context Pack) contains concrete values - no blanks, `...`, `TODO`, `TBD`, or angle-bracket placeholders. "N/A" is allowed with a task-specific reason.
- `Allowed Files` lists explicit subdirectories or file patterns (`src/auth/*.ts`, `src/export.py`). Broad wildcards (`*`, `**`, `.`, `src/*`) are rejected.
- `MAX_ITERATIONS` is an integer between 1 and 10.

## CLI validation

```bash
python scripts/check_task_pack.py docs/delivery/tasks/TASK-001.md --json
```

- Exit 0: `status: "passed"` - the pack is executable.
- Exit 1: `status: "failed"` - the `issues` array lists every structural blocker.
- Exit 2: the file could not be read (missing or unreadable path).

The JSON payload also carries a non-blocking `warnings` array (exit code unchanged): legacy v1.x packs missing `MAX_ITERATIONS`, and tautological test patterns (`assert True`, `assertTrue(True)`, commented-out assertions, empty `pass` test bodies) detected inside the Test Requirements section. Warnings are advisory: the main agent resolves them during the S14 test-quality review rather than at this gate.

## Test quality expectations (context for warnings)

Tests must assert behavior through public interfaces, cover acceptance criteria, include failure paths and edge cases for modified logic, and reuse the centralized client/service modules. Anti-patterns that trigger warnings or S14 rejection: empty test bodies, tautological assertions, HTTP-status-only checks, truthiness-only assertions, mocking the unit under test, and duplicating request logic across call sites.

## Manual fallback

If this skill's script is unavailable (not installed), check the pack against the readiness checklist above by hand and record the review in the pack's Status section.

For the full gate reference (16 required sections, blocking vs warning rules, and the S14 test-quality anti-pattern list), see `references/task-pack-gate.md`.
