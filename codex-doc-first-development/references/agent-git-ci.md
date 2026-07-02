# Agent, Git, and CI Coordination

Use this reference when the project uses subagents, branches, PRs, CI, or conflict handling.

## Agent Roles

Main Codex agent:

- Owns product and engineering interpretation.
- Chooses workflow mode.
- Creates or updates docs.
- Defines Task Packs.
- Spawns subagents only when authorized.
- Reviews and integrates subagent results.
- Runs or reviews verification.
- Produces final acceptance.

Explorer:

- Read-only.
- Answers one specific codebase or design question.
- Should not edit files.
- Should return evidence with paths and concise conclusions.

Worker:

- Edits files only inside assigned ownership.
- Handles one Task Pack.
- Must not revert or tidy unrelated changes.
- Must report changed files, tests, risks, and blockers.

Reviewer:

- Can be simulated by the main agent or an explorer.
- Reviews formal solution, docs, tests, or diff.
- Does not modify code unless explicitly assigned a fix task.

## Delegation Decision

Do not delegate:

- Immediate blocking work on the critical path.
- Tasks without clear ownership.
- Tasks that need constant product judgment.
- Work that writes shared contracts before those contracts are designed.

Delegate:

- Independent read-only investigation.
- Independent module implementation.
- Test creation for a bounded surface.
- Documentation cleanup separate from code writes.

## File Ownership Matrix

Before parallel work, produce:

```text
TASK-001:
  owns:
    - src/auth/**
    - tests/auth/**
  forbidden:
    - src/payments/**
    - docs/requirements.md
  shared:
    - docs/delivery/phase-001.md (main agent only)
```

Shared files should normally be edited by the main agent after workers return.

## Lock Protocol

Use a lock only when file ownership is not enough.

Lock fields:

- Path pattern.
- Owner task.
- Expiration time.
- Reason.
- Contact or responsible agent.

Example:

```yaml
locks:
  - path: src/auth/**
    owner: TASK-001
    expires_at: <ISO-8601 timestamp>
    reason: auth implementation
```

Treat expired locks as stale only after checking whether the owning work is still active.

## Branch Strategy

Quick mode:

- Current branch is acceptable when risk is low.

Standard mode:

- Prefer one feature branch.
- Name: `codex/<short-feature>`.

Strict mode:

- Phase branch: `codex/phase-001-<name>`.
- Task branch: `codex/task-001-<name>`.

Rules:

- Check worktree before branch operations.
- Do not overwrite uncommitted user changes.
- Rebase or merge only when the user/project strategy allows it.
- Do not push, force push, or delete remote branches without confirmation.

## Commit Strategy

Commit only when authorized. Keep commits scoped:

```text
docs: establish doc-first project plan
feat(auth): add login validation
test(auth): cover expired session behavior
fix(api): handle missing customer id
```

Include requirement or task IDs in commit body when useful.

## CI Strategy

Map checks by risk:

- Low risk: targeted command.
- Normal feature: lint/test/build or project equivalent.
- Strict: clean install or CI evidence.
- UI: screenshots or Playwright where visual behavior matters.
- Data: migration verification and rollback note.
- External services: mock, sandbox, or contract evidence.

Record:

```text
Command:
Environment:
Result:
Relevant output:
Skipped checks:
Reason:
```

## PR Preparation

Before PR:

- Verify branch state.
- Summarize changes by requirement.
- Include test evidence.
- Include screenshots/artifacts when relevant.
- Link docs updates.
- List risks and follow-ups.

PR body:

```markdown
## Summary

## Requirements

## Changes

## Tests

## Risks

## Screenshots / Artifacts

## Docs Updated
```

## Conflict Handling

Text conflict:

- Resolve markers.
- Preserve both valid behaviors when possible.
- Re-run tests.

Logic conflict:

- Compare against requirements and architecture.
- Choose behavior that satisfies documented contract.
- Update docs if the contract changed with authorization.

Test conflict:

- Do not delete tests just to pass.
- Merge test intent.
- Update fixtures carefully.

Docs conflict:

- Preserve facts from accepted work.
- Keep docs index current.
- Archive superseded decisions if needed.

## Blocked Conditions

Return `BLOCKED` when:

- Overlapping workers changed the same contract differently.
- CI cannot be interpreted.
- Required secrets or external accounts are missing.
- Current instructions require a destructive or high-risk operation.
- Requirements are internally inconsistent.
- The correct business decision is not derivable from docs or user instructions.
