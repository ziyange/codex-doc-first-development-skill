---
name: codex-doc-first-task-pack-gate
description: Use when creating, reviewing, or validating a Task Pack (TASK-###.md) before agent code execution: required sections, explicit Allowed Files granularity, MAX_ITERATIONS bounds, contract anchors, tautological-test rejection, and placeholder detection.
---

# Task Pack Gate

A Task Pack (`TASK-###.md`) records bounded execution scope; user authorization is separate. This skill checks structural readiness for Standard/Strict work and selected runtime protocols. Quick work can reuse an existing record or brief when no selected protocol requires a Task Pack.

## Readiness checklist

A Task Pack passes the gate only when all of the following hold:

- Title is `# TASK-###: <concrete title>`, and the ID matches the filename.
- All 16 required headings are present exactly once: Status, Requirement IDs, Objective, Context Pack, Must Read, Allowed Files, Forbidden Files, Interfaces / Contracts, Data Constraints, UI Constraints, Implementation Requirements, Test Requirements, Acceptance Criteria, Done Definition, Risks, Output Required.
- Requirement IDs contain at least one `REQ-###` reference.
- Every required section (except Context Pack) contains concrete values - no blanks, `...`, `TODO`, `TBD`, or angle-bracket placeholders. "N/A" is allowed with a task-specific reason.
- `Allowed Files` lists explicit subdirectories or file patterns (`src/auth/*.ts`, `src/export.py`). Broad wildcards (`*`, `**`, `.`, `src/*`) are rejected.
- When present, `MAX_ITERATIONS` is an integer between 1 and 10; missing legacy values produce warnings. Goal execution separately requires an explicit valid limit.

## CLI validation

```bash
python <skill-root>/scripts/check_task_pack.py <project-root>/docs/delivery/tasks/TASK-001.md --json
```

- Exit 0: `status: "passed"` - structural checks passed; verify authorization, dependencies, and applicable runtime gates before execution.
- Exit 1: `status: "failed"` - the `issues` array lists every structural blocker.
- Exit 2: the file could not be read (missing or unreadable path).
Here `<skill-root>` is this companion's installation directory; select the active Task Pack rather than assuming TASK-001. If blocked, report the failed check, affected work, and smallest repair. Preserve existing exit codes and JSON fields.

The JSON payload also carries a non-blocking `warnings` array (exit code unchanged): legacy v1.x packs missing `MAX_ITERATIONS`, and tautological test patterns (`assert True`, `assertTrue(True)`, commented-out assertions, empty `pass` test bodies) detected inside the Test Requirements section. Warnings are advisory: the main agent resolves them during the S14 test-quality review rather than at this gate.

## Test quality expectations (context for warnings)

Tests must assert behavior through public interfaces, cover acceptance criteria, include failure paths and edge cases for modified logic, and reuse the centralized client/service modules. Anti-patterns that trigger warnings or S14 rejection: empty test bodies, tautological assertions, HTTP-status-only checks, truthiness-only assertions, mocking the unit under test, and duplicating request logic across call sites.

## Manual fallback

If this skill's script is unavailable (not installed), check the pack against the readiness checklist above by hand and record the review in the pack's Status section.

For the full gate reference (16 required sections, blocking vs warning rules, and the S14 test-quality anti-pattern list), see `references/task-pack-gate.md`.
