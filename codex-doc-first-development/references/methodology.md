# Full Methodology

Use this reference when the user wants a complete document-first engineering workflow, not just a quick plan.

## Contents

- [Lifecycle Summary](#lifecycle-summary)
- [Startup, Intake, and Planning](#s0-startup-and-authorization)
- [Pre-Dev Product Prototyping & Docs Source of Truth](#s6-docs-source-of-truth-creation-and-pre-dev-ux-alignment)
- [Phase and Task Design](#s9-phase-plan-and-task-breakdown)
- [Spec-Driven Implementation and Validation](#s13-spec-driven-agent-implementation)
- [Acceptance and Change Control](#s16-main-agent-acceptance--code-doc-traceability)
- [Writeback, Merge, and Archive](#s20-documentation-writeback--knowledge-capture)

## Authority and Capability Boundaries

Follow higher-priority platform, user, and repository instructions before this methodology or generated project instructions. Treat approved docs as intended facts and reconcile them with code, tests, configuration, and runtime evidence.

This workflow does not provide a background scheduler, persistent lock or deadlock service, CI provider, GitHub integration, or automatic merge system. Use available tools explicitly, keep file ownership and locks as coordination protocols, and distinguish planned operations from executed evidence.

## Lifecycle Summary

```text
S0  Startup and authorization
S1  Raw idea capture, reflection, and feasibility check
S2  Project scan and current-state analysis
S3  Formal solution draft (Modular Independence & DRY Architecture)
S4  Independent solution review
S5  Formal solution finalization
S6  Docs source-of-truth creation & Pre-Dev UI/UX User Alignment (Image Gen)
S7  Docs review (Link & Schema Verification)
S8  Docs finalization & Baseline Lock
S9  Phase plan and task breakdown (Foundation First)
S10 Context Pack / Task Pack generation (Strict Spec Binding)
S11 Execution strategy selection
S12 Branch and concurrency control
S13 Spec-driven agent implementation (DRY & Contract Compliance)
S14 Test quality & DRY architecture review
S15 Local / sandbox / CI validation
S16 Main-agent acceptance & Code-Doc Traceability
S17 Git conflict handling
S18 Change classification & Synchronous Doc Sync
S19 Phase integration acceptance
S20 Documentation writeback & Knowledge Capture
S21 Merge / PR / release preparation
S22 Phase archive
```

## S0 Startup and Authorization

Capture:

- Project or task name.
- Autonomy Mode: Goal Mode (closed whitelist, max iterations), Plan Mode (phase-by-phase permission handshake), or Build Mode (stream execution).
- Allowed file modifications (`Allowed Files`).
- Branch creation permission.
- Subagent permission.
- GitHub / PR / CI permission.
- Dependency install and network permission.
- Commit and draft PR permission.
- Forbidden files, directories, systems, secrets, or production resources.

Derive authorization already established by the user or environment. Ask only about missing choices that change direction or permit material external or high-risk actions.

Output:

```text
Project / task:
Workflow mode: Goal / Plan / Build
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

## S1 Raw Idea Capture, Reflection, and Feasibility Check

Turn natural language into structured product input through mandatory self-reflection. Ask only for information that changes direction or resolves feasibility bottlenecks; otherwise record reasonable assumptions.

Mandatory Reflection & Feasibility Rules:
- **Never produce final specs immediately**: Upon receiving raw ideas, the agent's first block output MUST be `## CoT Intake Reflection`, detailing Missing Facts, Codebase Conflicts, and Technical Feasibility Bottlenecks.
- **Pain-Point Card Matching**: Match user input against 6 domain cards in `references/pain-points.md` using binary (0/1) feature hit score $S(C)$:
  $$S(C) = \frac{2.0 \times N_{\text{mandatory-hits}} + 1.0 \times N_{\text{pattern-hits}}}{2.0 \times N_{\text{mandatory-total}} + 1.0 \times N_{\text{pattern-total}}}$$
  Top-1 exclusivity applies for $S(C) \ge 0.5$.
- **Feasibility Verification**: Confirm that the requested feature can be realistically built under existing project constraints before writing formal architecture or docs.

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

Auto-Init Trigger:
Once sufficient information is gathered and feasibility is confirmed, automatically trigger project initialization (`python scripts/scaffold_docs.py --auto-detect`) to auto-populate `AGENTS.md` with detected stack commands (including Monorepo / sub-directory scan for Makefile, Dockerfile, pnpm-workspace, go.work, Cargo workspace, etc.) and create `docs/` source of truth.

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

## S3 Formal Solution Draft (Modular Independence & DRY Architecture)

Include:

- Background and goal.
- Current state.
- Users and scenarios.
- Scope and non-goals.
- **Functional Modules & Single Responsibility**:
  - Independent module boundaries with clear encapsulation.
  - **Unified API / Service Layer**: All data requests and external communication must be routed through centralized reusable modules (e.g. `ApiClient` or `DataService`). Forbid duplicate API call implementations.
  - **Backend Data Projection & Generic Filtering**: Backend endpoints must support dynamic field filtering (`fields=...` or projected query schemas) so one generic endpoint serves multiple consumer views without creating repetitive ad-hoc endpoints.
- Data objects and state transitions.
- **Interface & UI Architecture**:
  - Component hierarchy and page layout specifications.
  - UI Component-to-API Binding: explicit mapping of UI triggers -> API module -> parameters -> response fields -> loading/empty/error states.
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

Use in strict mode or when risk is high. Review only supplied materials and treat missing material as missing, not implied. Use an independent fresh-context reviewer only when subagents are authorized; otherwise run the same rubric as a disclosed main-agent self-review.

Score:

- Requirement clarity.
- Business loop completeness.
- Functional boundary quality & Modular Independence (DRY adherence).
- Architecture feasibility.
- Data and state completeness.
- Security and permission coverage.
- Interface and UI-API binding feasibility.
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

## S6 Docs Source-of-Truth Creation and Pre-Dev UX Alignment

Use mode-specific structure:

- Quick: minimum docs (`AGENTS.md`, `docs/README.md`, `docs/requirements.md`, `docs/delivery/TASK-001.md`).
- Standard: AGENTS, docs index, product, requirements, architecture, ux, delivery, verification, archive.
- Strict: standard plus decisions, locks, quality gates, and optional api/data-model/security/operations docs.

### Pre-Dev Product & UI/UX Interactive Alignment Gate (Mandatory before coding):
Before generating Phase Plans and Task Packs, the agent MUST communicate with the user to align on product design:
1. **Product Prototype & Navigation Flow**: Overall wireframe and user journey.
2. **Screen UI Layout & Views**: Specific layout for each screen, component breakdown, visual hierarchy.
3. **Component-to-API Binding Matrix**: Explicit table linking each UI component to its unified API module, request parameters, projected response fields, and UI feedback states.
4. **Interaction States**: Loading spinners, empty states, error banners, optimistic UI updates.
5. **Multimodal Image Generation (`generate_image`)**:
   - If the agent environment supports image generation tools (`generate_image` or multimodal generation), the agent MUST generate high-fidelity UI visual mockups for core product screens.
   - Save the generated images as project/artifact assets and embed them directly into `docs/ux.md` or `docs/product.md` using `![Screen Name UI Mockup](path/to/image.png)`.
   - If image generation tools are unavailable, fallback to structured ASCII wireframes and Mermaid UI flow diagrams.
6. **Full Documentation into `docs/`**: All agreed prototypes, UI layouts, API bindings, and interaction states must be recorded in `docs/ux.md` and `docs/architecture.md`.

Gate:

- Docs entry exists.
- Current requirements are traceable with `REQ-*` IDs.
- UX wireframes, UI layouts, and Component-API bindings are fully documented.
- Current validation is explicit.
- Codex can find all project facts from docs.

## S7 Docs Review

Review:

- Docs entry clarity.
- Requirement traceability.
- UI/UX and Component-to-API binding completeness.
- Modular independence and DRY service encapsulation.
- Acceptance testability.
- Architecture completeness.
- Task Pack executability.
- Test strategy executability.
- Subagent boundaries.
- Relative link and anchor validity (via `scripts/check_docs_links.py`).
- Automated script compliance and JSON output schemas.
- Branch and concurrency safety.
- Change handling.
- Archive completeness.

## S8 Docs Finalization & Baseline Lock

Fix docs review issues. Lock the documentation baseline (including UI mockups, interaction flows, and API contracts). Do not create decorative empty files.

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

- **Foundation First**: Shared infrastructure, unified API client / service modules, and common data models must be scheduled and implemented *before* dependent consumer features.
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
- Must-read documents (must explicitly include `docs/architecture.md`, `docs/ux.md`, and relevant `docs/requirements.md#REQ-*`).
- Allowed files (must list explicit subdirectories or file patterns, e.g. `src/auth/*.ts`; broad wildcards such as `*`, `**`, `.` are strictly rejected).
- Forbidden files.
- Interface/data/UI constraints (must reference centralized service modules and documented UI mockups/bindings).
- Implementation requirements (spec-driven, functional independence, DRY reusability).
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

Use multi-agent mode only after the user explicitly authorizes subagents. Otherwise keep the same Task Packs and execute them serially with the main agent.

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

## S13 Spec-Driven Agent Implementation

Implementation steps:

1. Read Task Pack.
2. Read must-read docs (verify API contracts, data models, UI wireframes, and component bindings).
3. Check allowed and forbidden files.
4. Check git status.
5. Read relevant code.
6. Add or update tests.
7. Run a failing check where practical.
8. Make small scoped edits complying strictly with documented contracts.
9. Run passing verification.
10. Report changed files, tests, risks.

Core Rules:

- **Strict Spec Compliance (严格按文档专项开发)**: Implement the exact function signatures, API routes, data fields, and UI component layouts documented in `docs/architecture.md`, `docs/ux.md`, and `docs/delivery/tasks/TASK-*.md`. Do not invent unapproved ad-hoc contracts.
- **Functional Independence & DRY Reusability (功能独立化 & 模块复用)**:
  - All data fetching and API communication must be encapsulated into a single reusable service/client module.
  - Consumers must import and call this module instead of writing duplicate fetch/axios/HTTP request logic in multiple places.
  - Backend/service handlers must support generic querying and field filtering/projection (e.g. `fields` parameter) so multiple views consume the same endpoint cleanly.
- Do not revert user changes.
- Do not overwrite other agents.
- Do not do unrelated refactors.
- Do not remove tests.
- Do not bypass business logic.
- Do not change unauthorized contracts.
- Follow local style.

## S14 Test Quality & DRY Review

Inspect whether tests prove behavior and code adheres to DRY architecture:

- Acceptance coverage.
- Meaningful assertions (no empty tests, tautological `assert True`, or unverified status codes).
- **DRY & Modular Independence Check**: Verify that data fetching logic is not duplicated across multiple components or caller sites.
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
- L4: GitHub PR checks or equivalent CI (consuming `--json` outputs from `check_task_pack.py` and `check_docs_links.py`).

Strict mode requires inspectable evidence. Label evidence as planned, locally executed, isolated, or externally executed. Never present a planned CI or PR check as completed; explain every skipped check.

## S16 Main-Agent Acceptance & Code-Doc Traceability

Inputs:

- Task Pack.
- Diff.
- Subagent output.
- Test output.
- CI / PR checks.
- Relevant docs (`docs/architecture.md`, `docs/ux.md`, `docs/requirements.md`).

Acceptance Rules:
- **Code-Doc Traceability Gate**: Cross-check the implementation against documented API signatures, data schemas, and UI interaction bindings. Reject changes if code diverges from documentation.
- **DRY Reusability Gate**: Verify that shared modules are properly reused and no duplicate API request boilerplate was introduced.

Statuses:

- `PASS`: Acceptance criteria met, verification passes, code matches docs, DRY respected.
- `REQUEST_CHANGES`: Local fix needed, test missing, duplicate code needs modularizing, or docs mismatch can be corrected immediately.
- `BLOCKED`: Requirements conflict, unapproved architectural divergence, missing permissions.

## S17 Git Conflict Handling

When conflicts appear:

1. Pause merge.
2. Read conflict files.
3. Compare against Task Pack, requirements, and architecture.
4. Resolve without deleting valid logic or tests.
5. Re-run relevant verification.
6. Record cause and resolution.
7. Re-enter acceptance.

## S18 Change Classification & Synchronous Doc Sync

Levels:

- Micro: no architecture, interface, data, or phase-plan impact.
- Standard: affects requirements, tests, or local implementation plan.
- Strict: affects architecture, data, security, milestone, or multiple tasks.

### Synchronous Two-Way Documentation Sync Rule:
Whenever user suggestions, feedback, or implementation adaptations lead to changes in:
- Functional architecture or module boundaries
- API signatures, routes, or query/response schemas
- Screen UI layouts, component structures, or visual mockups
- UI-to-API interaction bindings or state transitions

The agent MUST **synchronously update the corresponding project documents (`docs/architecture.md`, `docs/api.md`, `docs/ux.md`, `docs/requirements.md`, `TASK-*.md`) in the exact same step or prior to changing code**. Code changes must never outpace or diverge from documentation.

Strict changes require pausing affected work and asking the user to confirm.

## S19 Phase Integration Acceptance

Check:

- All tasks complete.
- All tasks passed main-agent acceptance.
- Task branches merged or ready.
- No code/interface/data conflict remains.
- Stage verification passes.
- Docs are updated and strictly aligned with code.
- Archive and release notes are ready.
- User confirmation obtained where required.

## S20 Documentation Writeback & Knowledge Capture

Write back:

- Requirement status.
- Architecture and module changes.
- UI mockups, interaction changes, and API bindings.
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
- Docs are updated and synchronized.
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
