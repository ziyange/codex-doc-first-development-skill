# Task Pack Gate

A Task Pack (`TASK-###.md`) records bounded execution scope. Use this checker when the project, user, or selected runtime protocol requires a formal Task Pack. Follow [Adaptive Workflow](adaptive-workflow.md) for other tasks. Update the pack's own status and add the verified result or an evidence link there; no separate acceptance report is needed.

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
Here `<skill-root>` is the main skill installation directory; select the active Task Pack rather than assuming TASK-001. If blocked, report the failed check, affected work, and smallest repair. Preserve existing exit codes and JSON fields.

The non-blocking `warnings` array flags missing `MAX_ITERATIONS` and dummy test patterns. Apply iteration requirements only for the selected protocol. Address relevant test warnings in the delivery review; warnings by themselves are neither a gate failure nor proof that tests passed.

## Test quality expectations (context for warnings)

Use the [delivery review](review-gates.md#before-delivering) to assess whether tests prove the changed behavior. This checker does not run the tests.

## Manual fallback

If the bundled script cannot run, report the dependency or installation problem. A manual readiness review can inform repairs, but record it separately from the executable gate and do not claim the gate passed.

For the full gate reference (16 required sections, blocking vs warning rules, and the S14 test-quality anti-pattern list), see `references/task-pack-gate.md`.
