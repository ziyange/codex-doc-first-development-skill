# Adaptive Workflow

This is the policy for selecting stages, records, and checks. Other references
describe how to run a selected stage. Respect higher-priority instructions,
existing project requirements, and explicit user choices.

## Choose a risk tier

Inspect project instructions, docs, change scope, and known authorization.
Choose by impact, regardless of file count, project age, or existing CI.

| Tier | Trigger | Verification |
|---|---|---|
| Quick | Clear, bounded, low-risk work, including small fixes with no architecture or public-contract impact | A focused check that proves the change, such as reviewing a wording diff or running a regression test |
| Standard | Feature, behavior, or cross-module changes that exceed Quick and do not trigger Strict | Verify the changed behavior across affected boundaries; run relevant project checks |
| Strict | Security, permissions, data migration, public contracts, major architecture, or material production risk | Review the specific risk and produce checkable evidence; cover relevant denial, failure, compatibility, or recovery behavior |

For Strict, use the evidence needed to assess the actual risk. For example, test
allowed and denied permission cases; rehearse a migration and its recovery in
isolation when feasible. Use independent review, full CI, or phase acceptance
when the risk warrants it or the project requires it. Reuse checks that already
cover the same acceptance criteria for the same change. Do not claim independent
review without an independent reviewer or delegate without authorization.

## Keep one closure record

A plan point is a result that can be accepted independently. A file edit,
command, or retry is not a new plan point. Multiple points may live in a single
plan or task table. Give each point one authoritative record:

- Before editing: objective, authorized scope and restrictions, observable
  acceptance criteria, and the check or evidence expected to prove them.
- After verifying: actual outcome (passed, needs changes, or blocked), the
  executed check or evidence location, and unresolved failures or limitations.
  Link to the test output, CI run/commit, or other source where available.
- Quick: use an existing task or plan entry if available. Otherwise state scope
  and the check at intake, then close in the final reply; no project file needed.
- Standard/Strict: prefer an existing writable task, issue, plan entry, or Task
  Pack that can hold the closure. Use an external record only with authorization.
  If none fits, add one compact Markdown task record in the project's existing
  task location, or under `docs/delivery/` when the project has no convention.
  A formal Task Pack is needed only when the project, user, or selected runtime
  protocol requires one. Use a phase plan when multiple outcomes need coordination.

A verification report, PR, or archive can point to the same evidence. Do not
copy the record into each of them. Store changed product and engineering facts
in their owning docs, before or alongside the implementation. Scaffolding is
for explicitly needed initialization; it is not a prerequisite.

## Use two review points

**Before editing:** Confirm existing authorization, scope, relevant contracts,
applicable project rules, and the verification approach in one pass. Align
unresolved designs only on changed surfaces. UI with no API documents events,
state, and outcomes. Non-graphical work skips visual proposals.

**Before delivering:** Review the change against its start state and verify the
same acceptance criteria. In Git, account for staged, unstaged, and new files,
preserving pre-existing work. Without Git, review the actual changed files.
Check owning docs for changed facts, resolve local fixes, and rerun only affected
or explicitly required checks. Count a manual check only for what was observed;
it cannot stand in for a required executable check. If required evidence is
missing or a check fails, record the gap and the smallest recovery action.

Reuse established authorization. If scope expands or risk rises, update the
record and stop only work dependent on unresolved authority or decisions.
A record, diff, or structural checker never grants authority.

## Keep runtime audit separate

Strict is a risk tier. Transaction logging is a separate protocol, selected by
existing project requirements, explicit user choice, or applicable audit rules.
Use the project's established audit mechanism. Only load [the bundled runtime
protocol](runtime-audit.md) when it is the selected mechanism. Ordinary host
planning, building, or goal tracking does not by itself select the skill's
Goal/Plan/Build protocols. Without the bundled protocol, do not create its
audit log, execution trace, expansions file, or lock just to satisfy this skill.

When the bundled protocol is active, preserve its inputs and fail-close behavior
even for Quick work. A closure record or final diff cannot replace an active
audit. Never recreate a missing record as empty to make a failed audit pass.
