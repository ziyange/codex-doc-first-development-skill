# Examples

Use these as patterns for how to apply the skill. Adapt artifact depth to risk.

## Contents

- [New SaaS MVP](#example-1-new-saas-mvp)
- [Existing Repo Feature](#example-2-existing-repo-feature)
- [Bug Fix](#example-3-bug-fix)
- [Refactor](#example-4-refactor)
- [Multi-Agent Phase](#example-5-multi-agent-phase)
- [Docs Recovery](#example-6-docs-recovery)

## Example 1: New SaaS MVP

User asks:

```text
Use $codex-doc-first-development to build a lightweight CRM for freelancers.
```

Recommended behavior:

- **Phase 1 (Intake & Reflection)**: Choose strict mode because this is a new project. Perform self-reflection: identify missing inputs (auth needs, database choice, deployment target), check potential conflicts, and verify technical feasibility.
- **Phase 2 (Clarification)**: Ask user to confirm essential direction-changing choices while documenting reasonable assumptions.
- **Phase 3 (Auto-Init)**: Once information is sufficient and feasibility is confirmed, automatically trigger project initialization (`python scripts/scaffold_docs.py --mode strict --phase 001 --auto-detect`) to create `AGENTS.md` and initial `docs/` source of truth.
- Generate `REQ-*` requirements, phase plan, and initial Task Packs for app shell, customer model, CRUD, and tests.

First output shape (Self-Reflection Response):

```text
Workflow mode: strict
Repository state: empty / new project
Information gaps & reflection: missing deployment target, auth requirement, data persistence choice
Feasibility & conflict checks: feasible under Node/TypeScript stack; no existing codebase collisions
Must-confirm: 1) Local DB vs Cloud DB? 2) Auth provider preference?
Reasonable assumptions: single-user MVP, local dev first
Recommended next step: clarify Must-Confirm items; upon response, Agent will auto-init AGENTS.md and docs/
```


## Example 2: Existing Repo Feature

User asks:

```text
Use $codex-doc-first-development to add export-to-CSV to this dashboard.
```

Recommended behavior:

- Choose standard mode unless the export touches sensitive data or permissions.
- Scan repo commands and dashboard architecture.
- Add `REQ-001` with acceptance criteria: visible export action, correct columns, filtered data, empty state, error path.
- Create `TASK-001` with allowed files.
- Add tests for transformation logic and UI interaction when available.
- Run targeted tests and build/typecheck.

## Example 3: Bug Fix

User asks:

```text
Use $codex-doc-first-development to fix the checkout total rounding bug.
```

Recommended behavior:

- Choose standard or strict depending on payment risk.
- Treat payment/checkout as high risk; likely strict.
- Capture expected rounding rule in `requirements.md`.
- Add failing test first.
- Fix smallest surface.
- Run payment-related tests plus build/typecheck.
- Record risk and skipped external payment checks.

## Example 4: Refactor

User asks:

```text
Use $codex-doc-first-development to refactor the auth module.
```

Recommended behavior:

- Choose strict if public auth behavior or permissions may change.
- Require non-goals: no behavior changes unless specified.
- Build Task Packs by module boundary.
- Add characterization tests before refactor.
- Use workers only for disjoint submodules.
- Main agent owns shared interfaces.

## Example 5: Multi-Agent Phase

User asks:

```text
I allow subagents. Use $codex-doc-first-development to build phase 1 in parallel.
```

Recommended behavior:

- Verify phase plan and Task Packs exist.
- Produce delegation plan before spawning.
- Assign explorers to read-only questions and workers to disjoint file scopes.
- Keep docs index, shared contracts, and integration under main agent.
- Review each worker diff before merging.
- Close subagents after review.
- Treat file ownership and locks as coordination protocols, not as a built-in persistent lock service.

## Example 6: Docs Recovery

User asks:

```text
Use $codex-doc-first-development to make this repo maintainable before adding features.
```

Recommended behavior:

- Choose standard mode.
- Scan repo.
- Create `AGENTS.md` and docs index.
- Recover product/requirements/architecture facts from README, code, tests, and package config.
- Mark uncertain items as assumptions or open questions.
- Do not invent product facts.
