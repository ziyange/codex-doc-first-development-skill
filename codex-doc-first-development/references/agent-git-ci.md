# Agent, Git, and CI Coordination

Use only the capabilities that the user and project authorize. This reference
applies when subagents, branches, CI, PRs, or conflicts need coordination.

## Roles and ownership

The main agent owns scope, shared contracts, integration, and acceptance.
An explorer reads for a specific question; a worker implements one bounded
outcome with a disjoint write scope; a reviewer checks a particular risk or
decision. Use subagents only with authorization. A main-agent self-review is
useful but is not independent.

Use the existing task or plan to list allowed files, exclusions, and the owner
of shared files. Leave tightly coupled or blocking work with the main agent.
Add an advisory lock only if file ownership alone cannot avoid overlap. Record
its owner, path scope, reason, and expiry; check whether the owner is active
before treating an expired lock as stale.

## Branches, conflicts, and commits

Check the starting worktree, preserve unrelated user changes, and follow the
project's branch policy. Use separate branches only when required or useful
for isolation. Rebase, merge, commit, or push only within established scope
and authorization. For a conflict, preserve each side's valid behavior, check
against governing docs, and rerun affected verification after resolution.

## CI and handoff

Use [Adaptive Workflow](adaptive-workflow.md) to select verification and
[review gates](review-gates.md) to interpret the result. Link CI evidence for
the revision delivered. Distinguish planned, local, isolated, and external
evidence; a local command is not a PR check.

Prepare a PR by describing the change and linking the existing task, checks,
and material risks. Add screenshots or artifacts only when they help review.
If the necessary checks, authority, or inputs are missing, record the blocker
with the affected plan point and identify the smallest recovery step.
