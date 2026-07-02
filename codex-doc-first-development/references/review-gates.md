# Review Gates

Use these gates to decide whether work can move from planning to docs, docs to implementation, implementation to acceptance, and acceptance to merge/archive.

## Mode Selection

Use quick mode when all are true:

- Change is small and low risk.
- Scope is obvious.
- A full docs structure would add more overhead than clarity.
- Verification is simple.

Use standard mode when any are true:

- Change spans multiple files or modules.
- Requirements need tracking.
- Tests or docs need meaningful updates.
- A future maintainer needs context.

Use strict mode when any are true:

- New project or architecture change.
- Security, permissions, payment, data migration, deployment, or public API risk.
- Multi-agent or parallel development.
- CI/PR/release process matters.
- Failure has high user or business impact.

## Formal Solution Review

Score or inspect these dimensions before building docs in strict mode:

| Dimension | Pass Condition |
|---|---|
| Requirements clarity | Goals, users, scope, non-goals, and acceptance criteria are clear |
| Business loop | Main workflows have a complete start, action, outcome, and failure path |
| Functional boundaries | MVP and later work are separated |
| Architecture feasibility | Modules, contracts, and dependencies are implementable |
| Data and state | Data objects and state changes are explicit when relevant |
| Security and permissions | Sensitive flows and access rules are addressed |
| Interface/integration | API, UI, CLI, or integration contracts are defined |
| Testability | Acceptance criteria map to verification methods |
| Codex executability | Work can be decomposed into clear tasks |
| Subagent safety | Parallel tasks have non-overlapping write scopes |
| CI feasibility | Required checks can run in available environments |
| Rollback/change control | Risks, rollback, and change levels are defined |

Do not proceed when a blocking issue affects architecture, data, security, or acceptance.

## Docs Review

Docs can support implementation when:

- `docs/README.md` points to active requirements, phase, tasks, verification, and archive.
- Current requirements have `REQ-*` IDs.
- Acceptance criteria are testable.
- The phase plan names tasks and dependencies.
- Each Task Pack has allowed and forbidden files.
- Test strategy and expected commands are explicit.
- Agent collaboration rules are present when subagents are used.
- Merge and high-risk operation rules require user confirmation.

## Task Pack Gate

A Task Pack is executable only if it includes:

- Task ID and status.
- Requirement IDs.
- Objective.
- Must-read context.
- Allowed files.
- Forbidden files.
- Interfaces/contracts or "not applicable".
- Data/UI constraints or "not applicable".
- Implementation requirements.
- Test requirements.
- Acceptance criteria.
- Done definition.
- Required final output.

## Test Quality Gate

Good tests:

- Cover acceptance criteria.
- Assert behavior, state, output, or side effects.
- Include failure paths or edge cases where relevant.
- Avoid mocking the core behavior being tested.
- Can run reliably in local or CI environments.

Weak or invalid tests:

- `assert(true)` or equivalent.
- Only checks HTTP 200 without content or state.
- Checks only non-null output when exact behavior matters.
- Mocks away the business logic under test.
- Does not verify permission, error, or boundary behavior for risky flows.

## Validation Levels

| Level | Evidence |
|---|---|
| L1 | Local targeted test or focused manual check |
| L2 | Local lint/test/typecheck/build as applicable |
| L3 | Clean worktree, clean install, container, or sandbox-style validation |
| L4 | GitHub PR checks, Actions, review comments, or equivalent CI evidence |

Use the highest level proportional to risk. Record why any expected check was skipped.

## Acceptance Status

Return `PASS` when:

- Acceptance criteria are satisfied.
- Verification evidence is sufficient.
- Diff is scoped.
- Docs are updated or intentionally unchanged.
- Known risks are acceptable.

Return `REQUEST_CHANGES` when:

- A fix is clear and local to the current task.
- Tests or docs are missing but can be added.
- Diff includes unrelated changes that can be removed safely.

Return `BLOCKED` when:

- Requirements conflict with existing facts.
- Permissions, credentials, network, or dependencies are missing.
- CI is unstable and cannot be interpreted.
- Subagent work overlaps or overwrites state.
- Main Codex cannot reliably decide correctness.
- A high-risk operation needs user confirmation.

## Merge Gate

Do not prepare final merge or release until:

- Task or phase acceptance is `PASS`.
- Worktree status is understood.
- Tests/CI are passing or failures are documented and accepted.
- Docs writeback is complete.
- Conflicts are resolved.
- Main branch merge, push, publication, deletion, or history rewrite has explicit user confirmation.

## Archive Gate

Archive at phase end:

- Phase summary.
- Completed and incomplete requirements.
- Task Packs.
- Verification evidence.
- Decisions and ADRs.
- Change records.
- Conflict or blocked reports.
- Known issues.
- Next-phase recommendations.

