# Bundled Runtime Audit

Read this only when the project or user selects this skill's audit mechanism.
Follow [Adaptive Workflow](adaptive-workflow.md) for ordinary acceptance and
authorization. This protocol checks the submitted artifacts; it does not prove
that every action was recorded or grant authority.

## Modes and inputs

- Goal: closed whitelist, bounded iteration. The active Task Pack must contain
  exactly one `MAX_ITERATIONS: N` line with N in 1..10.
- Plan: phase-by-phase authorization, closed whitelist, and a single-step commit
  for `MODE_SWITCH`.
- Build: stream execution against the existing blacklist. Do not select Build
  or switch modes to bypass an active constraint.
- Preserve the active Task Pack, allowed and forbidden files, expansion and
  mode-switch rules, and the initialized trace and log. Initialize an empty
  audit log and a trace containing `[]` only before the first action of a
  fresh audit. Missing, unreadable, or invalid mandatory inputs block progress.

Resolve helpers from the skill installation, and inputs from the project. Run
the required verification before proceeding or finalizing, at the checkpoints
of the selected protocol. Supply the active Task Pack, actual project input
paths if they differ from the defaults, and the current iteration for Goal:

```text
python <skill-root>/scripts/verify_runtime_trace.py --task-pack <active-task-pack> --mode goal --next-iteration 1 --json
```

The example uses the first Goal iteration. Use the actual mode and iteration.
The bundled JSON schemas are authoritative; see [schemas](schemas.md) for the
Markdown fallback. The checker keeps its existing exit codes and JSON contract.

## Transactions

Use `scripts/lock_manager.py` to coordinate single-writer access to
`docs/delivery/.log.lock`, with PID and timestamp-based stale lock handling.
Write a PENDING Intent before the authorized action; transition it to COMMITTED
or ABORTED. Write the matching Result for a completed non-`PERMISSION_GRANT`
action. The chain uses
`SHA256(prev_hash + ":" + action_type + ":" + normalized_path + ":" + tx_id)`.
`scripts/check_permission_log.py` checks the chain statically. Expansions must be
authorized and anchored by a committed `PERMISSION_GRANT`; the existing limit
is two per task. See [the schema reference](schemas.md) for input fields.

## Exit handling

| Exit | Signal | Action |
|---|---|---|
| 0 | `SUCCESS` | Submitted trace and audit checks pass; proceed if otherwise authorized |
| 1 | `ITERATION_EXCEEDED` | Stop autonomous iteration and report the blocker |
| 2 | `EXPANSION_LIMIT_EXCEEDED` | Stop Goal execution and downgrade to Plan as required by the protocol |
| 2 | Other boundary violation | Inspect `offending_files`; request authorization if the scope must expand |
| 3 | `SCHEMA_OR_PARSE_FAILURE` | Stop and repair the required inputs or environment |
| 4 | `SAFELY_ABORTED_OPERATION` | Report the safe abort; retry only within established authority |
| 4 | Other transaction gap | Read `reason_details`. For `UNCOMMITTED_PENDING`, reconcile actual action state before retrying or aborting. For `COMMITTED_RESULT_MISSING`, recover the Result only; do not repeat the action. For `RESULT_WITHOUT_INTENT`, discard the orphan and reconcile the audit log |
| 5 | `TAMPER_OR_HASH_MISMATCH` | Stop and report the integrity failure |
| 6 | `ILLEGAL_TRANSACTION_STATE` | Stop and require manual reconciliation |
