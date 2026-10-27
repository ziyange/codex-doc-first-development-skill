# Review Gates

Use these gates to decide whether work can move from planning to docs, docs to implementation, implementation to acceptance, and acceptance to merge/archive.
Apply [Adaptive Workflow](adaptive-workflow.md) first: select stages by risk, retain selected runtime protocols, and review only changed applicable surfaces. Existing user authorization is reused; structural checks do not create authorization.

## Contents

- [Mode Selection](#mode-selection)
- [Formal Solution and Pre-Dev UX Gate](#formal-solution-review)
- [Task Pack Gate](#task-pack-gate)
- [Test Quality and DRY Reusability](#test-quality--dry-reusability-gate)
- [Acceptance, Merge, and Archive](#acceptance-status--code-doc-traceability)

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

- Major architecture change or material production risk; a new project alone does not force Strict.
- Security, permissions, payment, data migration, deployment, or public API risk.
- Public contract changes.
- Parallel work or CI/PR activity alone does not force Strict; evaluate its security, data, and production impact.
- Failure has high user or business impact.

## Information Sufficiency & Feasibility Gate

Apply this gate during initial intake before Agent auto-initialization (`/init` / `scaffold_docs.py`):

| Check Item | Pass Criterion | Required Action if Failed |
|---|---|---|
| **Self-Reflection** | Mandatory reflection executed; no critical ambiguity in core user goals or scope. | Ask user targeted clarifying questions; do not generate final specs. |
| **Codebase Conflict** | Proposed change evaluated against existing codebase structure and dependencies without unhandled collisions. | Raise conflict warning to user; adjust architectural boundaries. |
| **Feasibility Bottlenecks** | Solution is technically achievable under given stack, OS, performance, and permission limits. | Flag feasibility risk as `BLOCKED` or suggest alternative technical path. |


## Formal Solution Review

Score or inspect these dimensions before building docs in strict mode:

| Dimension | Pass Condition |
|---|---|
| Requirements clarity | Goals, users, scope, non-goals, and acceptance criteria are clear |
| Business loop | Main workflows have a complete start, action, outcome, and failure path |
| Functional boundaries | MVP and later work are separated |
| Architecture feasibility | Modules, contracts, and dependencies are implementable |
| **Modular Independence & DRY** | Reuse modules for shared requests; use projection only for demonstrated requirements; no duplicated request logic |
| Data and state | Data objects and state changes are explicit when relevant |
| Security and permissions | Sensitive flows and access rules are addressed |
| Interface/integration | API, UI, CLI, or integration contracts are defined |
| Testability | Acceptance criteria map to verification methods |
| Codex executability | Work can be decomposed into clear tasks |
| Subagent safety | Parallel tasks have non-overlapping write scopes |
| CI feasibility | Required checks can run in available environments |
| Rollback/change control | Risks, rollback, and change levels are defined |

Do not proceed when a blocking issue affects architecture, data, security, or acceptance.

## Pre-Dev Product UI/UX & API Alignment Gate (Mandatory Before Coding)

Apply to changed graphical UI surfaces in S6-S8 before dependent implementation. Reuse approved designs; non-UI tasks skip visual artifacts and verify their own contracts. Local-only UI records events/state/outcomes rather than API bindings.

| Check Item | Pass Criterion | Required Action if Failed |
|---|---|---|
| **Product Prototype & Flow** | Wireframes and screen navigation paths are confirmed by user. | Re-align with user on page hierarchy and user flow. |
| **Screen UI Layouts** | Component breakdown, form controls, and responsive layouts are defined for all core screens. | Draft UI layouts in `docs/ux.md` and confirm with user. |
| **UI-to-API Binding Table** | Every UI trigger / component is mapped to its centralized API module, parameters, projected response fields, and UI feedback states. | Complete the UI-API binding matrix in `docs/ux.md`. |
| **Multimodal UI Preview** | Unresolved visual decisions have suitable mockups/wireframes; approved designs are reused. | Generate only the affected visual proposal using available tools. |
| **Full Documentation** | All agreed UI layouts, bindings, and states are fully recorded in project docs (`docs/ux.md`, `docs/architecture.md`). | Write specs into `docs/` before proceeding to S9. |

## Docs Review

Docs can support implementation when:

- `docs/README.md` points to active requirements, phase, tasks, verification, and archive.
- Current requirements have `REQ-*` IDs.
- Affected graphical UI designs/states and applicable API bindings are documented in the owning UX doc; local UI uses events/state/outcomes.
- Acceptance criteria are testable.
- The phase plan names tasks and dependencies (prioritizing shared infrastructure and reusable modules).
- Each Task Pack has allowed and forbidden files and explicit Must-Read contract anchors.
- Test strategy and expected commands are explicit.
- Agent collaboration rules are present when subagents are used.
- All relative Markdown links and heading anchors are verified valid via `check_docs_links.py` in the `codex-doc-first-doc-sync` companion skill (apply the GFM anchor rules manually if that skill is unavailable).
- Automated check scripts pass or produce JSON Schema compliant `--json` payloads for CI/CD pipelines: `check_task_pack.py` and `check_docs_links.py` from their own companion skills (`codex-doc-first-task-pack-gate`, `codex-doc-first-doc-sync`), `scaffold_docs.py` and `verify_runtime_trace.py` from this skill.
- Merge and high-risk operation rules require user confirmation.

## Task Pack Gate

A Task Pack is executable only if it includes:

- Task ID and status.
- Requirement IDs.
- Objective.
- Must-read context (including explicit architecture and UI-API binding anchors).
- Allowed files.
- Forbidden files.
- Interfaces/contracts (referencing unified client/service modules) or "not applicable".
- Data/UI constraints (referencing documented UI specs) or "not applicable".
- Implementation requirements (enforcing spec-driven development & DRY reusability).
- Test requirements.
- Acceptance criteria.
- Done definition.
- Risks, including an explicit "none identified" when appropriate.
- Required final output.

Required sections must contain concrete values rather than blank text, `...`, `TODO`, `TBD`, or angle-bracket placeholders. Interfaces, data constraints, and UI constraints may say "not applicable" only with a task-specific reason.

`Allowed Files` must specify explicit subdirectories or file patterns (e.g. `src/auth/*.ts`, `src/export.py`). Overly broad wildcards (such as `*`, `**`, or `.`) are strictly rejected.

## Test Quality & DRY Reusability Gate

Good tests & implementation:

- Cover acceptance criteria.
- Assert behavior, state, output, or side effects.
- Include failure paths, edge cases, and boundary conditions for modified logic.
- Avoid mocking the core behavior being tested.
- **DRY Reusability**: Reuses centralized data client / service modules without duplicating API call logic in multiple places.
- Can run reliably in local or CI environments.

Weak or invalid tests (Strictly Rejected Anti-Patterns):

- Empty test functions or tests without assertions (e.g., `def test_foo(): pass`).
- `assert True`, `assertTrue(True)`, or `expect(true).toBe(true)`.
- HTTP status checks (e.g., checking status code 200) without verifying payload, state, or contract facts.
- Checking only non-null/truthy output when exact field values or behavior matter.
- Mocks that replace the actual unit/component under test instead of its dependencies.
- Omitting boundary, permission, or error path test coverage for changed logic.
- Introducing duplicate network request boilerplate instead of calling the centralized service module.

## Validation Levels

| Level | Evidence |
|---|---|
| L1 | Local targeted test or focused manual check |
| L2 | Local lint/test/typecheck/build as applicable |
| L3 | Clean worktree, clean install, container, or sandbox-style validation |
| L4 | GitHub PR checks, Actions, review comments, or equivalent CI evidence |

Use the highest level proportional to risk. Record why any expected check was skipped.

Label every result as planned, locally executed, isolated, or externally executed. A command listed in a plan is not evidence that it ran.

## Runtime Trace Verification & Exit Code Protocol (0–6)

Strict work and explicitly selected runtime protocols are verified via `scripts/verify_runtime_trace.py`. Other Quick/Standard work uses proportional checks under the adaptive policy. The main agent evaluates runtime output using the following Exit Code Table and **Exhaustive 8-Row Dispatch Lookup Table**:

### Exit Code Table (0–6)
| Exit Code | Identifier | Validation Rule | Main-Agent SKILL.md Action |
|:---:|---|---|---|
| `0` | `SUCCESS` | Trace, AuditLog, and Merkle chain valid | **Pass**: Proceed with current iteration execution. |
| `1` | `ITERATION_EXCEEDED` | `--next-iteration k > MAX_ITERATIONS` | **Circuit-Break Halt**: Terminate autonomous self-healing, report `BLOCKED`. |
| `2` | `OFF_BOUNDARY_VIOLATION` | Unauthorized file edit or expansion limit ($> 2$) | **Issue Expansion or Downgrade**: If expansion limit reached, force downgrade to Plan mode; else request user expansion. |
| `3` | `SCHEMA_OR_PARSE_FAILURE` | Schema missing, log corrupt, or JSON invalid | **Fail-Close**: Halt immediately, prompt user to repair environment. |
| `4` | `UNCOMMITTED_TRANSACTION` | `UNCOMMITTED_PENDING`, `COMMITTED_RESULT_MISSING`, or `SAFELY_ABORTED_OPERATION` | **Transaction Recovery**: Parse `runtime_event_reason` and `reason_details` for node-specific action. |
| `5` | `TAMPER_OR_HASH_MISMATCH` | Merkle chain link broken, SHA256 mismatch, or forged trace | **Security Alert (Short-circuit)**: Halt immediately, alert audit log corruption. |
| `6` | `ILLEGAL_TRANSACTION_STATE` | `PENDING+Present` or `ABORTED+Present` contradiction | **Data Audit (Short-circuit)**: Halt immediately, request manual audit. |

### Exhaustive 8-Row Main-Agent Dispatch Lookup Table
| `exit_code` | `runtime_event_reason` | Scenario Description | Main-Agent SKILL.md Dispatch Action |
|:---:|:---:|---|---|
| `1` | `null` | Iteration limit exceeded | **Circuit-Break Halt**: Terminate autonomous loop, report `BLOCKED`. |
| `2` | `"EXPANSION_LIMIT_EXCEEDED"` | Expansion count exceeded limit (max 2) | **Fuse & Downgrade**: Force downgrade Goal mode to Plan mode. |
| `2` | `null` | File edit out of whitelist boundary | **Issue Expansion**: Parse `offending_files`, request user expansion approval. |
| `3` | `null` | Schema missing, file corrupt, or parse failure | **Fail-Close**: Halt immediately, prompt user to repair environment. |
| `4` | `"SAFELY_ABORTED_OPERATION"` | Lock write exception safely aborted to ABORTED | **Safe Retry**: Inform user action was safely aborted, allow action retry. |
| `4` | `null` | Static chain node contains `Exit 4` gap | **Fallback Dictionary Parse**: Parse `reason_details`: for `UNCOMMITTED_PENDING` retry action or abort; for `COMMITTED_RESULT_MISSING` **write Result trace ONLY, DO NOT retry action**. |
| `5` | `null` | Merkle chain broken, hash mismatch, or trace tampered | **Security Alert (Short-circuit)**: Halt immediately, alert audit log corruption. |
| `6` | `null` | `PENDING+Present` or `ABORTED+Present` contradiction | **Data Audit (Short-circuit)**: Halt immediately, request manual audit. |

## Acceptance Status & Code-Doc Traceability

Return `PASS` when:

- Acceptance criteria are satisfied.
- **Code-Doc Traceability**: Implemented code strictly adheres to documented API contracts, data models, and UI component bindings.
- **DRY Compliance**: Data requests use the unified client/service module with no duplicate endpoints or duplicate call logic.
- **Synchronous Doc Sync**: All architectural, API, or interaction changes made during development are fully reflected in `docs/`.
- Verification evidence is sufficient.
- Diff is scoped.
- Known risks are acceptable.

Return `REQUEST_CHANGES` when:

- A fix is clear and local to the current task.
- Implementation diverges from documented contracts or UI specs.
- Duplicate API request logic was introduced instead of reusing the centralized module.
- Architecture/API/UI was modified without updating corresponding `docs/` files.
- Tests or docs are missing but can be added.
- Diff includes unrelated changes that can be removed safely.

Return `BLOCKED` when:

- Requirements conflict with existing facts.
- Permissions, credentials, network, or dependencies are missing.
- CI is unstable and cannot be interpreted.
- Subagent work overlaps or overwrites state.
- Main Codex cannot reliably decide correctness.
- A high-risk operation needs user confirmation.

Before returning `BLOCKED`, exhaust safe in-scope checks and alternatives and identify the exact unresolved conflict, permission, evidence gap, or decision.

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
