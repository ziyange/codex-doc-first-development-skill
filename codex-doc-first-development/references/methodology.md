# Full Methodology

Use this reference when the user wants a complete document-first engineering workflow, not just a quick plan.

## Lifecycle Summary

```text
S0  Startup and authorization
S1  Raw idea capture
S2  Project scan and current-state analysis
S3  Formal solution draft
S4  Independent solution review
S5  Formal solution finalization
S6  Docs source-of-truth creation
S7  Docs review
S8  Docs finalization
S9  Phase plan and task breakdown
S10 Context Pack / Task Pack generation
S11 Execution strategy selection
S12 Branch and concurrency control
S13 Agent implementation
S14 Test quality review
S15 Local / sandbox / CI validation
S16 Main-agent acceptance
S17 Git conflict handling
S18 Change classification
S19 Phase integration acceptance
S20 Documentation writeback
S21 Merge / PR / release preparation
S22 Phase archive
```

## S0 Startup and Authorization

Capture:

- Project or task name.
- Existing repository or new project.
- Allowed file modifications.
- Branch creation permission.
- Subagent permission.
- GitHub / PR / CI permission.
- Dependency install and network permission.
- Commit and draft PR permission.
- Forbidden files, directories, systems, secrets, or production resources.

Output:

```text
Project / task:
Workflow mode:
Authorization:
Known restrictions:
High-risk operations:
Must-confirm questions:
Reasonable assumptions:
Later questions:
Next step:
```

Never execute by default:

- Merge to main.
- Push to remote main.
- Force push.
- Delete remote branches.
- Reset Git history.
- Publish production release.
- Delete user files.
- Overwrite uncommitted user changes.

## S1 Raw Idea Capture

Turn natural language into product input. Ask only for information that changes direction; otherwise record assumptions.

Capture:

- Problem.
- Target users.
- Current workaround.
- Core scenarios.
- MVP scope.
- Non-goals.
- Success criteria.
- Platform, time, budget, technical constraints.
- Design, brand, performance, security, compliance constraints.
- Delivery shape: site, app, API, CLI, library, plugin, automation.

Artifact: `docs/product.md`.

## S2 Project Scan and Current-State Analysis

For new projects, determine:

- Suggested stack.
- Project structure.
- Build tool.
- Test framework.
- Deployment model.
- Database, authentication, external service needs.
- CI needs.

For existing projects, inspect:

- `README`.
- `docs`.
- `AGENTS.md`.
- package/build config.
- test directories.
- CI config.
- architecture entry points.
- code style.
- git status and uncommitted changes.

Output:

```text
Project type:
Main stack:
Run command:
Test command:
Build command:
Key directories:
Engineering conventions:
Git state:
Uncommitted changes:
Risks:
Recommended workflow mode:
```

## S3 Formal Solution Draft

Include:

- Background and goal.
- Current state.
- Users and scenarios.
- Scope and non-goals.
- Functional modules.
- Data objects and state transitions.
- Interfaces, pages, interactions, or CLI/API contracts.
- Technical implementation path.
- Codex execution boundaries.
- Workflow mode.
- Branch strategy.
- Subagent strategy.
- Test and validation strategy.
- Risks and rollback.
- Phase plan.
- Deliverables.
- Requirement traceability matrix.
- Open questions.

Artifacts:

- `formal-solution.md` when strict mode needs a durable draft.
- `requirement-traceability-matrix.md` when requirements are numerous or regulated.

## S4 Independent Solution Review

Use in strict mode or when risk is high. Review only supplied materials. Treat missing material as missing, not implied.

Score:

- Requirement clarity.
- Business loop completeness.
- Functional boundary quality.
- Architecture feasibility.
- Data and state completeness.
- Security and permission coverage.
- Interface and integration feasibility.
- Test and acceptance executability.
- Documentation traceability.
- Codex executability.
- Subagent decomposability.
- Branch and concurrency safety.
- CI / validation feasibility.
- Change and rollback ability.

Proceed only when no blocking issues remain.

## S5 Formal Solution Finalization

Incorporate valid review findings into the final plan. Do not output a comparison or revision history; output the current formal solution.

## S6 Docs Source-of-Truth Creation

Use mode-specific structure:

- Quick: minimum docs.
- Standard: AGENTS, docs index, product, requirements, architecture, delivery, verification, archive.
- Strict: standard plus ADRs, API/data/security/UX/operations docs, locks, quality gates.

Gate:

- Docs entry exists.
- Current requirements are traceable.
- Current validation is explicit.
- Codex can find the project facts from docs.

## S7 Docs Review

Review:

- Docs entry clarity.
- Requirement traceability.
- Acceptance testability.
- Architecture completeness.
- Task Pack executability.
- Test strategy executability.
- Subagent boundaries.
- Branch and concurrency safety.
- Change handling.
- Archive completeness.

## S8 Docs Finalization

Fix docs review issues. Keep docs factual and current. Do not create decorative empty files.

## S9 Phase Plan and Task Breakdown

Every phase defines:

- Goal.
- Scope and non-goals.
- Requirement IDs.
- Tasks.
- Dependencies.
- Branch strategy.
- Agent strategy.
- Test strategy.
- Acceptance gate.
- Risks.
- Archive path.

Task splitting rules:

- One clear goal per task.
- Independent acceptance per task.
- Disjoint write scopes for parallel tasks.
- Shared contracts designed before implementation.
- High-risk tasks get early spikes or validation.

## S10 Context Pack / Task Pack Generation

Each Task Pack must include:

- `TASK-*` ID.
- Status.
- Related `REQ-*` IDs.
- Objective.
- Must-read documents.
- Allowed files.
- Forbidden files.
- Interface/data/UI constraints.
- Implementation requirements.
- Test requirements.
- Acceptance criteria.
- Done definition.
- Risks.
- Required output.

No worker may modify code without a Task Pack.

## S11 Execution Strategy Selection

Single-agent mode for:

- Small tasks.
- Highly coupled work.
- Critical path decisions.
- No subagent authorization.

Multi-agent mode for:

- Independent modules.
- Read-only exploration.
- Test and implementation separation.
- Docs and code work that can safely run in parallel.

## S12 Branch and Concurrency Control

Recommended branch names:

```text
codex/phase-001-short-name
codex/task-001-short-name
codex/fix-short-name
```

Concurrency protocol:

- Task Pack declares allowed and forbidden files.
- Parallel writes must not overlap.
- Shared files are edited by the main agent.
- Use `docs/delivery/locks.yml` only when useful.

## S13 Agent Implementation

Implementation steps:

1. Read Task Pack.
2. Read must-read docs.
3. Check allowed and forbidden files.
4. Check git status.
5. Read relevant code.
6. Add or update tests.
7. Run a failing check where practical.
8. Make small scoped edits.
9. Run passing verification.
10. Report changed files, tests, risks.

Rules:

- Do not revert user changes.
- Do not overwrite other agents.
- Do not do unrelated refactors.
- Do not remove tests.
- Do not bypass business logic.
- Do not change unauthorized contracts.
- Follow local style.

## S14 Test Quality Review

Inspect whether tests prove behavior:

- Acceptance coverage.
- Meaningful assertions.
- Success path.
- Failure path.
- Boundary conditions.
- Permission and error cases where relevant.
- Stable execution.
- CI compatibility.

## S15 Local / Sandbox / CI Validation

Levels:

- L1: local targeted command.
- L2: local lint/test/typecheck/build.
- L3: clean worktree, clean install, container, or sandbox.
- L4: GitHub PR checks or equivalent CI.

Strict mode requires inspectable evidence. Skipped checks need reasons.

## S16 Main-Agent Acceptance

Inputs:

- Task Pack.
- Diff.
- Subagent output.
- Test output.
- CI / PR checks.
- Relevant docs.

Statuses:

- `PASS`.
- `REQUEST_CHANGES`.
- `BLOCKED`.

## S17 Git Conflict Handling

When conflicts appear:

1. Pause merge.
2. Read conflict files.
3. Compare against Task Pack, requirements, and architecture.
4. Resolve without deleting valid logic or tests.
5. Re-run relevant verification.
6. Record cause and resolution.
7. Re-enter acceptance.

## S18 Change Classification

Levels:

- Micro: no architecture, interface, data, or phase-plan impact.
- Standard: affects requirements, tests, or local implementation plan.
- Strict: affects architecture, data, security, milestone, or multiple tasks.

Strict changes require pausing affected work and asking the user to confirm.

## S19 Phase Integration Acceptance

Check:

- All tasks complete.
- All tasks passed main-agent acceptance.
- Task branches merged or ready.
- No code/interface/data conflict remains.
- Stage verification passes.
- Docs are updated.
- Archive and release notes are ready.
- User confirmation obtained where required.

## S20 Documentation Writeback

Write back:

- Requirement status.
- Architecture changes.
- New commands.
- Test strategy changes.
- Decisions.
- Known limitations.
- Phase acceptance.
- Change records.

Do not rewrite entire docs unless necessary. Prefer targeted patches.

## S21 Merge / PR / Release Preparation

Gate:

- Acceptance is `PASS`.
- Worktree state is clear.
- Tests/CI pass or risk is documented.
- Docs are updated.
- Conflicts are resolved.
- Main branch merge is confirmed by user.

## S22 Phase Archive

Archive:

- Phase summary.
- Task Packs.
- Verification evidence.
- Acceptance records.
- Change records.
- Known issues.
- Roadmap update.

Then either return to S9 for the next phase or move to release/maintenance/closeout.

