# Prompt Pack

Use these prompts as starting points. Adapt them to the repository, user authorization, and workflow mode.

## Contents

- [Start From Zero](#start-from-zero)
- [Existing Repository Intake](#existing-repository-intake)
- [Formal Solution and Docs](#formal-solution)
- [Pre-Dev UI/UX and Prototype Alignment](#pre-dev-uiux-and-prototype-alignment)
- [Phase and Delegation](#phase-plan)
- [Worker Execution](#worker-task)
- [Acceptance and Change Control](#acceptance-review)
- [Synchronous Doc Sync on Change](#synchronous-doc-sync-on-change)

## Start From Zero

```text
Use $codex-doc-first-development as the main workflow.

Project idea:
<<<paste idea>>>

Authorization:
- Modify files: yes/no
- Create Git branches: yes/no
- Create subagents: yes/no
- Use GitHub/PR/CI: yes/no
- Install dependencies or use network: yes/no
- Commit changes: yes/no
- Create draft PR: yes/no

First:
1. Output the first response block as `## CoT Intake Reflection` containing:
   - Missing Facts
   - Codebase Conflicts
   - Feasibility Bottlenecks
2. Ask clarifying questions for missing inputs; do not generate final specs immediately.
3. Once sufficient information is gathered and feasibility is verified, automatically trigger initialization (`scaffold_docs.py --auto-detect`) to create AGENTS.md and docs source of truth.
4. Design independent functional modules & unified API service layer to eliminate duplicate requests (DRY).
5. Align with the user on product prototypes, screen UI layouts, API bindings, and interaction states (generate visual UI mockup images if image generation tool is available).
6. Choose quick, standard, or strict mode.
7. Draft the phase plan and task breakdown with narrow Allowed Files scoping.
8. Explain whether subagents are useful.
```


## Existing Repository Intake

```text
Use $codex-doc-first-development to plan this change in the current repository.

Goal:
<<<task goal>>>

Constraints:
<<<constraints>>>

Please scan README, docs, AGENTS.md, package/build/test config, tests, CI, architecture entry points, and git status before proposing changes.

First:
1. Output the initial response block as `## CoT Intake Reflection` containing:
   - Missing Facts
   - Codebase Conflicts
   - Feasibility Bottlenecks
2. Output workflow mode, risks, docs updates needed, modular service architecture (DRY check), test strategy, branch strategy, and the first Task Pack with narrow Allowed Files scoping.
```

## Formal Solution

```text
Create a formal implementation solution from the project idea and repository scan.

Required sections:
1. Background and goal
2. Current state
3. Users and scenarios
4. Scope and non-goals
5. Requirements and acceptance criteria
6. Architecture and module boundaries (Functional Independence & Centralized Service Layer)
7. Data, interface, UI layout, and Component-to-API binding matrix
8. Test and validation strategy
9. Branch and PR strategy
10. Subagent strategy
11. Risks and rollback
12. Phase breakdown (Foundation First)
13. Requirement traceability matrix
14. Open questions
```

## Pre-Dev UI/UX and Prototype Alignment

```text
Prior to beginning code implementation, present the product prototype and UI/UX design to the user for confirmation:

1. Product Prototype: Show navigation flow and screen hierarchy.
2. Screen UI Layouts: Detail page components, form inputs, and layout structure.
3. Multimodal Preview: If image generation tools (e.g. generate_image) are supported, generate high-fidelity UI visual mockups for key screens and embed them in docs/ux.md.
4. Component-to-API Binding Matrix:
   | Screen / Component | User Action | Unified API Module / Route | Request Parameters | Projected Fields | UI State (Loading/Empty/Error) |
5. Interaction Design: Specify user feedback, transitions, and error recovery flows.
6. Record all finalized designs into docs/ux.md and docs/architecture.md.
```

## Docs Source of Truth

```text
Create or update the Codex-optimized docs source of truth.

Mode:
quick / standard / strict

Requirements:
- Create or update AGENTS.md.
- Create or update docs/README.md as the docs entry point.
- Create or update product, requirements, architecture, ux, delivery, verification, and archive docs according to the mode.
- Give every current requirement a REQ ID.
- Ensure unified client/service modules and backend field projection are specified.
- Record UI layouts, component bindings, and interaction states.
- Make acceptance criteria verifiable.
- Do not create empty decorative documents.
- Create optional strict-mode documents only when applicable facts exist.
```

## Phase Plan

```text
Generate the current phase plan.

Include:
1. Phase goal, scope, and non-goals.
2. Related REQ IDs.
3. Task list with TASK IDs (Foundation & shared API/service modules scheduled first).
4. Allowed and forbidden files for each task.
5. Test requirements and acceptance criteria.
6. Parallel vs serial task classification.
7. Suggested subagents, if authorized and useful.
8. Branch strategy.
9. Archive path.
```

## Subagent Authorization Plan

```text
I allow subagents for parallel work.

Before spawning any subagent, list:
1. Agent type: explorer or worker.
2. Task.
3. Reads.
4. Allowed files.
5. Forbidden files.
6. Acceptance criteria.
7. How the main Codex agent will review results.

Only create workers for disjoint write scopes. Keep shared files under the main Codex agent.
```

## Worker Task

```text
You are a Codex worker. You are not alone in the codebase.
Do not revert, overwrite, or tidy changes unrelated to your task.

Task Pack:
<<<paste Task Pack>>>

Rules:
1. Read only the required context unless you need adjacent code to implement safely.
2. Modify only allowed files.
3. Do not modify forbidden files.
4. Strictly implement the exact API contracts, signatures, and UI component structures documented in Must Read docs.
5. Functional Independence & DRY: Use the centralized API/service module for network calls; do not write duplicate request logic.
6. Do not expand scope.
7. Add or update tests according to the Task Pack.
8. Run required verification commands.
9. If requirements, interfaces, data, tests, or file ownership conflict, output BLOCKED.

Final output:
1. Changed files.
2. Implementation summary.
3. Test commands and results.
4. Unfinished items.
5. Risks.
6. Recommendation for main-agent acceptance.
```

## Acceptance Review

```text
Enter Codex main-agent acceptance mode.

Inputs:
- Task Pack
- git diff
- Subagent output, if any
- Test output
- CI/PR checks
- Docs changes

Rules:
1. Do not accept agent self-report as the only evidence.
2. Code-Doc Traceability: Verify that implemented code strictly adheres to documented API contracts, data models, and UI component bindings.
3. DRY Reusability: Verify that centralized service modules were used and no duplicate API request boilerplate was introduced.
4. Check every acceptance criterion.
5. Check whether tests have meaningful assertions.
6. Check for unrelated changes.
7. Check whether docs need writeback or synchronous sync.
8. Output PASS, REQUEST_CHANGES, or BLOCKED.
9. Label evidence as planned, locally executed, isolated, or externally executed.
```

## Change Control

```text
Classify this new request during active development.

Change:
<<<change request>>>

Current context:
<<<phase/task/status>>>

Classify as:
- micro: does not affect architecture, interface, data, or phase plan
- standard: affects requirements, tests, or local implementation plan
- strict: affects architecture, data, security, milestone, or multiple tasks

Output impact, docs updates, task updates, agent impact, verification impact, and whether user confirmation is required.
```

## Synchronous Doc Sync on Change

```text
User requested a modification or feedback during development.

Change Details:
<<<change details>>>

Sync Protocol:
1. Identify affected documents: docs/architecture.md, docs/api.md, docs/ux.md, docs/requirements.md, or TASK-*.md.
2. Synchronously update the corresponding documentation sections in docs/ BEFORE or IN PARALLEL with code modifications.
3. Implement code changes adhering strictly to the newly updated document contracts.
4. Run validation and acceptance checking to ensure code and docs remain in 100% lockstep.
```
