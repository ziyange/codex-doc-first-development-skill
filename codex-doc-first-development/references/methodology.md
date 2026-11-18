# Full Methodology

This lifecycle index expands the stages that an agent can use. Start with
[Adaptive Workflow](adaptive-workflow.md) to choose the applicable stages,
record, and checks. Group stages that can be completed in the same pass.

## Contents

- [Intake and solution (S0–S5)](#s0-startup-and-authorization)
- [Docs and task design (S6–S10)](#s6-docs-source-of-truth-creation-and-pre-dev-ux-alignment)
- [Implementation and verification (S11–S16)](#s11-execution-strategy-selection)
- [Integration and handoff (S17–S22)](#s17-git-conflict-handling)

## S0 Startup and Authorization

Derive what can be read, changed, and executed from the user and project rules.
Keep approvals for Git pushes, merges, deployments, and other external actions
separate from task acceptance. Reuse approval for the same action and scope.

## S1 Intake and Feasibility

Inspect missing facts, conflicts, and feasibility. Tell the user the proposed
scope and checks. Consult [domain cards](pain-points.md) when relevant and ask
only about unresolved choices that change what can safely be delivered.

## S2 Repository Scan

Inspect affected docs, code paths, tests, build config, project instructions,
and the starting worktree. If initialization is needed, preview the scaffold
command in the skill entrypoint and inspect its output before writing.

## S3 Formal Solution Draft

Where design is needed, define the expected behavior, relevant contracts, module
boundaries, dependencies, and failure or rollback paths. Reuse shared clients
and introduce data projection only for a demonstrated need.

## S4 Solution Review

Use the [preflight criteria](review-gates.md#before-editing) to check design
decisions that could affect feasibility, risk, or acceptance. An independent
review is useful when the stakes or project requirements warrant it.

## S5 Solution Finalization

Put agreed product and engineering decisions into the owning docs. Reuse
prior decisions and reference them from the task instead of copying them.

## S6 Docs Source-of-Truth Creation and Pre-Dev UX Alignment

For changed graphical UI, consult [UI/UX guidance](ui-ux-prototyping.md). Align
only unresolved layouts, interactions, and states. API-backed UI documents
changed bindings; local-only UI documents its changed events and state.

## S7 Docs Review

Check affected facts and references with [doc sync guidance](doc-sync.md) as
part of the before-editing or before-delivering pass, as applicable.

## S8 Docs Finalization and Baseline

Identify the references that govern the change. Use their current revisions;
a separate baseline file or lock is unnecessary unless the project requires one.

## S9 Phase Plan and Task Breakdown

When several outcomes need coordination, order dependencies before consumers
and give each independently verifiable outcome a row or referenced task in the
same plan. Keep the result and evidence with that outcome.

## S10 Context Pack / Task Pack Generation

Use an existing scoped record. When a formal Task Pack is required, follow
[its structural checker](task-pack.md). A passing checker is not authorization.

## S11 Execution Strategy Selection

Use the available agent and tooling. Use workers only with authorization and
disjoint write scopes. Use the bundled [runtime audit](runtime-audit.md)
only when selected under the adaptive policy.

## S12 Branch and Concurrency Control

Follow [project coordination guidance](agent-git-ci.md) if applicable. Choose
branches or locks when they address actual ownership or isolation needs.

## S13 Spec-Driven Agent Implementation

Read governing contracts and stay within scope. Keep owned docs in step with
changed facts. Preserve user changes and reuse shared implementation.

## S14 Test Quality and Reusability

Use assertions that check the changed behavior, including relevant boundary and
failure paths. Check the affected shared modules for duplicated logic.

## S15 Local, Isolated, or CI Validation

Run the checks chosen for the task. Record actual outcomes or link the evidence.
See [review gates](review-gates.md) for deciding whether evidence is sufficient.

## S16 Main-Agent Acceptance and Traceability

Compare actual changes and evidence to the authorized scope, acceptance criteria,
and owning docs in a single delivery review. Update the existing closure record.

## S17 Git Conflict Handling

Preserve valid changes from both sides, verify affected behavior after the
resolution, and add a material conflict or risk to the existing record.

## S18 Change Classification and Doc Sync

When facts, risk, or scope change, revisit the applicable parts of the adaptive
policy and update the current record. Use [doc sync](doc-sync.md) for ownership.

## S19 Phase Integration Acceptance

If integration is a separate acceptance outcome, verify cross-task behavior
and dependencies once. Link completed task evidence from the phase plan.

## S20 Documentation Writeback and Knowledge Capture

Write back changed facts to their source documents. Capture a reusable lesson
only if it will change future decisions; routine execution belongs in the task.

## S21 Merge, PR, or Release Preparation

Check the required acceptance and branch state for the change being published.
Link existing results. Re-run checks only when affected or required for the
revision being merged. Preserve the applicable authorization requirements.

## S22 Phase Archive

Archive only when the project needs a handoff or retention record. Prefer a
summary with pointers to existing tasks, verified results, and open issues.
