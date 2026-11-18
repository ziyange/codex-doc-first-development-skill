# Review Gates

Use [Adaptive Workflow](adaptive-workflow.md) to select checks and the closure
record. These criteria guide two review points; use relevant parts in a single
pass and record the result with the existing plan point.

## Before editing

- The outcome, allowed scope, and authority are clear. Verify the project
  baseline and relevant dependencies before promising an implementation.
- Changed requirements and contracts have an owner. For unresolved design,
  review feasibility, boundaries, data handling, compatibility, and recovery
  only where they change implementation. Use [UI/UX guidance](ui-ux-prototyping.md)
  for affected graphical surfaces.
- Acceptance is observable with available tools. Map each material risk to the
  check that would detect it. Use [Task Pack validation](task-pack.md) if
  required; scorecards and standalone review reports are not prerequisite.
- Carry forward project or user-required checks, including the
  [bundled runtime audit](runtime-audit.md) only when that protocol is active.

## Before delivering

1. Compare actual changes with the starting state and allowed scope. Consider
   staged and new files as well as unstaged changes. Preserve unrelated work.
2. Check that requirements, contracts, and relevant docs match the change.
   For shared requests, review reuse and avoid duplicate request logic.
3. Match actual verification to acceptance. Tests should assert behavior,
   payloads, state, or side effects. Use relevant boundary and failure cases;
   tautologies, empty tests, and mocks of the behavior under test are not proof.
4. Record a single outcome: `PASS` when required checks and criteria pass,
   `REQUEST_CHANGES` when a local fix remains, or `BLOCKED` when a required
   decision, permission, dependency, or check prevents delivery. Identify
   the smallest recovery step. Recheck affected or required checks after a fix.

## Choose useful verification

Focused manual checks can confirm copy, layout, or other observable results.
Use behavior tests, lint, type checks, or a build when they address the change
or are required. For Strict work, match evidence to the specific risk: denial
and allowed cases for access changes; representative data and a recovery
rehearsal when feasible for migrations; compatibility for public contracts.

Use clean installs, isolated environments, independent review, or CI when
required or when a concrete risk cannot be resolved with local evidence. A
required executable gate cannot be replaced by manual review. Distinguish
planned, local, isolated, and external checks. Link real outputs when possible.

## Handoff

For a PR, merge, or phase handoff, refer to the existing closure record and
use evidence for the revision being delivered. Confirm applicable project
rules and existing authorization; acceptance does not authorize an external
action. Archive or produce an independent report only when required or when
it serves a specific handoff need. Link existing evidence instead of copying it.
