---
name: codex-doc-first-development
description: Use when running document-first software development, planning bounded implementation tasks, synchronizing changed contracts with docs, or requiring verifiable engineering governance. Adapt documentation and design gates to task risk while preserving explicit authorization and runtime audit requirements.
---

# Codex Doc-First Development (v3.0.0 Released)

## Operating Model

Treat this skill as the main engineering workflow guide within higher-priority platform, user, and repository instructions. Use it to convert vague intent into durable project facts, then into bounded tasks, then into verified code changes.
Install only this directory. Start with `$codex-doc-first-development` plus a task, or let the agent select it when appropriate. Intake, doc sync, Task Pack checks, and UI guidance are bundled here.
Read `references/adaptive-workflow.md` first: select applicable stages and artifacts by risk, reuse existing authorization/docs, and apply UI gates only to graphical UI changes. S0-S22 is the lifecycle index, not a required artifact list for every task.

Keep three layers separate; never let execution facts replace product or engineering facts. If implementation reveals a new fact, write it back to the correct document:
- Product facts: user, problem, scenarios, scope, non-goals, success criteria, UI mockups, interaction flows.
- Engineering facts: architecture, reusable modules, contracts, commands, tests, risks, branch strategy.
- Execution facts: phase plan, Task Packs, allowed files, verification evidence, acceptance, archive.

---

## Core Rules & Governance Protocols

1. **Orthogonal Autonomy Modes**:
   - **Goal Mode**: Closed whitelist, autonomous iteration up to `MAX_ITERATIONS` ($1 \le N \le 10$). Triggers circuit breaker on $k > N$.
   - **Plan Mode**: Phase-by-phase permission handshake. Single-step commit for `MODE_SWITCH`.
   - **Build Mode**: Low-overhead stream execution against blacklist patterns (`.git/*`, `permission-audit.log`, `.log.lock`, etc.).

2. **Domain Pain-Point Card Matching**:
   - When domain-specific inspection is relevant, compute binary feature hit score $S(C)$ against 6 domain cards (`references/pain-points.md`); communicate findings and decisions concisely.
   - $S(C) \ge 0.8$: enforce the card's inspection checklist. $0.5 \le S(C) < 0.8$: require `user_confirmed: true`. Top-1 exclusivity: activate only the highest card $\ge 0.5$, log the rest in `ignored_candidates`.

3. **Functional Independence & DRY Reusability (功能独立化 & 模块复用)**:
   - **Centralized Service/Client Layer**: Encapsulate all data fetching and external API calls into dedicated single modules (e.g. `client.ts` / `service.py`). Forbid duplicating the same request logic across multiple components or caller sites.
   - **Backend Projection & Field Filtering**: Use projection when actual consumer/performance needs justify it; preserve existing contracts and do not introduce endpoints for template compliance.
   - **DRY Gate**: Reject code changes that implement identical or near-identical request logic in multiple places.

4. **Pre-Dev Interactive UI/UX Design Gate & Image Generation (开发前产品UI/交互深度沟通与生图联动)**:
   - For graphical UI changes, read `references/ui-ux-prototyping.md`, align changed layouts/states before implementation, and reuse approved designs.
   - Record changed layouts/bindings/states in the owning docs; use mockups when visual decisions need alignment. Non-UI tasks skip this gate; local UI records events/state without invented APIs.

5. **Strict Spec-Driven Targeted Development (严格按文档专项开发)**:
   - During S13, code must strictly implement the exact contracts, signatures, field names, and UI structures documented in `docs/` and `TASK-*.md`. Ad-hoc deviation or skipping documented specs is strictly forbidden.
   - Foundation/shared modules must be implemented and tested before dependent consumer features.

6. **Synchronous Two-Way Documentation Sync (架构/接口/交互变动同步联动回写)**:
   - When user feedback, suggestions, or technical discoveries cause changes in architecture, API contracts, UI layouts, or interactions, the agent MUST synchronously update the corresponding documentation files under `docs/` (`docs/architecture.md`, `docs/api.md`, `docs/ux.md`, `docs/requirements.md`, `TASK-*.md`) in the exact same step or prior to code changes.
   - Acceptance gate (S16) strictly blocks PRs/commits where code contracts diverge from documentation.

7. **Machine-First Standalone JSON Schemas**:
   - Load JSON schemas directly from the standalone JSON files in the schemas directory (5 schemas), with Markdown fallback.

8. **Executable Merkle Chain Runtime Verification & Lock Manager**:
   - For Strict work or explicit runtime audit protocols, run `scripts/verify_runtime_trace.py` before proceeding or finalizing; Quick does not waive a selected protocol.
   - Computes SHA256 chain: `intent_hash_n = SHA256(prev_hash_n + ":" + action_type_n + ":" + normalized_path_n + ":" + tx_id_n)`.
   - Enforces `docs/delivery/.log.lock` single-writer file mutex locking using `lock_manager.py` with PID & timestamp stale lock cleanup.

## Exit Code Protocol (0–6) & Exhaustive Main-Agent Dispatch Table

Main agent handles non-Exit-0 CLI outputs by strictly looking up the `(exit_code, runtime_event_reason)` tuple:

| `exit_code` | `runtime_event_reason` | Scenario Description | Main-Agent SKILL.md Dispatch Action |
|:---:|:---:|---|---|
| `0` | `null` | AuditLog, Trace, and Merkle chain fully valid | **Pass**: Proceed with current iteration execution. |
| `1` | `null` | Iteration limit exceeded (`k > MAX_ITERATIONS`) | **Circuit-Break Halt**: Terminate autonomous self-healing, report `BLOCKED`. |
| `2` | `"EXPANSION_LIMIT_EXCEEDED"` | Expansion count exceeded limit (max 2) | **Fuse & Downgrade**: Force downgrade Goal mode to Plan mode. |
| `2` | `null` | File edit out of whitelist boundary | **Issue Expansion**: Parse `offending_files`, request user expansion approval. |
| `3` | `null` | Schema missing, file corrupt, or parse failure | **Fail-Close**: Halt immediately, prompt user to repair environment. |
| `4` | `"SAFELY_ABORTED_OPERATION"` | Lock write exception safely aborted to ABORTED | **Safe Retry**: Inform user action was safely aborted, allow action retry. |
| `4` | `null` | AuditLog contains uncommitted transaction | **Fallback Dictionary Parse**: Parse `reason_details`: `UNCOMMITTED_PENDING` retry action or abort; `COMMITTED_RESULT_MISSING` write Result trace ONLY, DO NOT retry action; `RESULT_WITHOUT_INTENT` discard the orphan Result and reconcile the audit log. |
| `5` | `null` | Merkle chain broken, hash mismatch, or trace tampered | **Security Alert (Short-circuit)**: Halt immediately, alert audit log corruption. |
| `6` | `null` | `PENDING+Present` or `ABORTED+Present` contradiction | **Data Audit (Short-circuit)**: Halt immediately, request manual audit intervention. |

## Workflow Modes & Risk Levels

| Mode | Risk Level | Required Artifacts | Verification Gate |
|---|---|---|---|
| Quick | Low | Reuse existing record or one brief; selected runtime protocols retain full inputs | Relevant command check |
| Standard | Medium | Affected docs + Task Pack; phase plan for multiple tasks; UI bindings when applicable | Task Pack structural gate + relevant tests |
| Strict | High / Critical | Full applicable docs + runtime audit; UX only for UI changes | `scripts/verify_runtime_trace.py --json` + tests |

---

## Main Workflow (S0 – S22)

1. **S0 Permission & Handshake**: Establish authorization scope and initial workflow mode.
2. **S1 Intake & Feasibility**: Inspect missing facts, conflicts and feasibility; report tier, scope and checks, asking only material unresolved questions.
3. **S2 Repository Context Scan**: Inspect existing docs/code first. When initialization is needed, run `python <skill-root>/scripts/scaffold_docs.py --root <project-root> --auto-detect --dry-run`; inspect before rerunning without `--dry-run`.
4. **S3 Formal Solution Draft**: Create architecture, data model, and interface specs with independent module & DRY design.
5. **S4 Solution Review**: Verify against `references/review-gates.md`.
6. **S5 Solution Finalization**: Update `docs/product.md` and `docs/architecture.md`.
7. **S6 Docs Source-of-Truth & Applicable UX Alignment**: Reuse/update applicable docs; for graphical UI changes read `references/ui-ux-prototyping.md`. Non-UI work skips visual artifacts.
8. **S7 Docs Review**: Read `references/doc-sync.md`; run `python <skill-root>/scripts/check_docs_links.py <project-root>/docs --json` over the affected tree.
9. **S8 Docs Finalization & Baseline Lock**: Lock initial documentation including UI layouts and API bindings.
10. **S9 Phase Plan Breakdown**: Create `docs/delivery/phase-001.md` prioritizing shared modules.
11. **S10 Task Pack Generation**: Read `references/task-pack.md`; create the applicable scoped Task Pack and run `python <skill-root>/scripts/check_task_pack.py <active-task-pack> --json`.
12. **S11 Strategy Selection**: Select Goal, Plan, or Build mode.
13. **S12 Branch & Concurrency Setup**: Create feature branch and locks.
14. **S13 Spec-Driven Implementation**: Follow authorized contracts and scope; maintain audit/trace inputs when the selected protocol requires them.
15. **S14 Test Quality & DRY Review**: Verify test coverage, meaningful assertions, and absence of duplicate request logic.
16. **S15 Runtime Gate Validation**: From the project root, execute `python <skill-root>/scripts/verify_runtime_trace.py --mode <mode> --json`; bundled schemas resolve from the skill directory. Set `--task-pack` to the active Task Pack.
17. **S16 Acceptance Decision & Doc-Code Traceability**: Inspect Exit Code and verify code-to-doc contract consistency.
18. **S17 Git Conflict Handling**: Resolve branch merge conflicts cleanly.
19. **S18 Change Classification & Synchronous Doc Sync**: Categorize changes; synchronously update `docs/` on architecture/API/UI changes.
20. **S19 Phase Acceptance**: Validate phase completion against `phase-xxx.md`.
21. **S20 Knowledge & Doc Writeback**: Sync final facts into docs and reusable patterns into `references/pain-points.md`.
22. **S21 Merge / PR Preparation**: Prepare PR summary with verified CLI trace outputs and updated docs checklist.
23. **S22 Phase Archive**: Archive phase outputs to `docs/archive/`.

---

## Scripted Helpers Summary

- `scripts/verify_runtime_trace.py`: Verifies runtime trace, Merkle chain, two-phase commit, and exit codes 0-6.
- `scripts/check_permission_log.py`: Internal module for static Merkle chain verification.
- `scripts/scaffold_docs.py`: Scaffolds mode-specific documentation directory skeletons.

- `scripts/check_task_pack.py`: Checks Task Pack structure and emits advisory warnings; does not grant execution authority.
- `scripts/check_docs_links.py`: Checks Markdown relative links and GFM heading anchors.
- `scripts/lock_manager.py`: Coordinates single-writer audit access.

---

## Bundled Guidance

Load the relevant internal reference as needed; no other skill installation or Skill-tool handoff is required:

| Step | Reference | Covers |
|---|---|---|
| S0 / S1 | `references/session-start.md` | one entry point, intake, scope, existing authorization |
| S6 | `references/ui-ux-prototyping.md` | applicable layouts, bindings, states, mockups |
| S7 / S18 / S20 | `references/doc-sync.md` | link/anchor validation, doc sync, writeback |
| S10 | `references/task-pack.md` | Task Pack structural readiness gate |

If a bundled script cannot run, report the missing dependency or damaged installation; do not claim its executable gate passed from a manual checklist.

---

## References

For full operational specifications, load these single-source reference documents:
- `references/schemas.md`: 5 authoritative JSON Schemas; the standalone JSON files in the schemas directory are the machine-readable authority and are loaded first by the scripts.
- `references/capabilities-matrix.md`: S0-S22 lifecycle asset mapping.
- `references/pain-points.md`: 6 domain pain-point cards.
- `references/methodology.md`: Full S0-S22 lifecycle methodology.
- `references/review-gates.md`: Full gate definitions and exit code tables.
- `references/templates.md`: Artifact templates.
- `references/prompts.md`: Reusable prompt templates.
- `references/agent-git-ci.md`: Multi-agent Git and CI coordination.
- `references/examples.md`: Reference implementations and examples.
