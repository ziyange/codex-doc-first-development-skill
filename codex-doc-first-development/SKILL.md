---
name: codex-doc-first-development
description: Guides Codex through document-first software development v2.3.0 with strict spec-driven targeted development, functional independence & DRY modularization, pre-dev interactive UI/UX prototyping with image generation capability, synchronous two-way doc sync on user feedback, Merkle runtime verification (Exit 0-6), composable companion skills (doc-sync, task-pack-gate, ui-ux-prototyping), and full lifecycle (S0-S22) governance. Use when starting software projects, formalizing AI development methodology, scaffolding docs, bounding multi-agent tasks, or executing verifiable software development.
---

# Codex Doc-First Development (v2.3.0 Released)

Use this skill to execute a Codex-specific, document-first software development process from idea intake through implementation, validation, merge preparation, and archival.

## Operating Model

Treat this skill as the main engineering workflow guide within higher-priority platform, user, and repository instructions. Use it to convert vague intent into durable project facts, then into bounded tasks, then into verified code changes.

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
   - During `CoT Intake Reflection`, compute binary feature hit score $S(C)$ against 6 domain cards (`references/pain-points.md`).
   - $S(C) \ge 0.8$: enforce the card's inspection checklist. $0.5 \le S(C) < 0.8$: require `user_confirmed: true`. Top-1 exclusivity: activate only the highest card $\ge 0.5$, log the rest in `ignored_candidates`.

3. **Functional Independence & DRY Reusability (功能独立化 & 模块复用)**:
   - **Centralized Service/Client Layer**: Encapsulate all data fetching and external API calls into dedicated single modules (e.g. `client.ts` / `service.py`). Forbid duplicating the same request logic across multiple components or caller sites.
   - **Backend Projection & Field Filtering**: Backend/service layers provide generic querying and dynamic field filtering (e.g., `fields` projection) so multiple UI views reuse the same generic endpoint rather than proliferating redundant ad-hoc endpoints.
   - **DRY Gate**: Reject code changes that implement identical or near-identical request logic in multiple places.

4. **Pre-Dev Interactive UI/UX Design Gate & Image Generation (开发前产品UI/交互深度沟通与生图联动)**:
   - After requirements and API architecture are drafted, **prior to code implementation**, align with the user on prototypes, screen layouts, component-to-API bindings, and interaction states (delegate to the `codex-doc-first-ui-ux-prototyping` companion skill).
   - Record all layouts, bindings, and states in `docs/ux.md` or `docs/architecture.md`; when image generation tools are available, proactively generate high-fidelity mockups for core screens and embed them via `![UI Mockup](...)` in `docs/ux.md`.

5. **Strict Spec-Driven Targeted Development (严格按文档专项开发)**:
   - During S13, code must strictly implement the exact contracts, signatures, field names, and UI structures documented in `docs/` and `TASK-*.md`. Ad-hoc deviation or skipping documented specs is strictly forbidden.
   - Foundation/shared modules must be implemented and tested before dependent consumer features.

6. **Synchronous Two-Way Documentation Sync (架构/接口/交互变动同步联动回写)**:
   - When user feedback, suggestions, or technical discoveries cause changes in architecture, API contracts, UI layouts, or interactions, the agent MUST synchronously update the corresponding documentation files under `docs/` (`docs/architecture.md`, `docs/api.md`, `docs/ux.md`, `docs/requirements.md`, `TASK-*.md`) in the exact same step or prior to code changes.
   - Acceptance gate (S16) strictly blocks PRs/commits where code contracts diverge from documentation.

7. **Machine-First Standalone JSON Schemas**:
   - Load JSON schemas directly from the standalone JSON files in the schemas directory (5 schemas), with Markdown fallback.

8. **Executable Merkle Chain Runtime Verification & Lock Manager**:
   - Run `scripts/verify_runtime_trace.py` for hard gate checks before proceeding or finalizing.
   - Computes SHA256 chain: `intent_hash_n = SHA256(prev_hash_n + ":" + action_type_n + ":" + normalized_path_n + ":" + tx_id_n)`.
   - Enforces `docs/delivery/.log.lock` single-writer file mutex locking using `lock_manager.py` with PID & timestamp stale lock cleanup.

---

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

---

## Workflow Modes & Risk Levels

| Mode | Risk Level | Required Artifacts | Verification Gate |
|---|---|---|---|
| Quick | Low | Task Pack or brief note | Single relevant command check |
| Standard | Medium | Minimal docs source of truth + Phase plan + Task Pack + UI/API Binding | Task Pack gate (`codex-doc-first-task-pack-gate`) + unit tests |
| Strict | High / Critical | Full docs source of truth + UX Mockups + Merkle trace audit | `scripts/verify_runtime_trace.py --json` |

---

## Main Workflow (S0 – S22)

1. **S0 Permission & Handshake**: Establish authorization scope and initial workflow mode.
2. **S1 Intake & CoT Reflection**: Execute CoT intake analysis, compute pain-point card confidence score $S(C)$.
3. **S2 Repository Context Scan**: Run `python <skill-root>/scripts/scaffold_docs.py --root <project-root> --auto-detect --dry-run`; inspect the proposed files before rerunning without `--dry-run`.
4. **S3 Formal Solution Draft**: Create architecture, data model, and interface specs with independent module & DRY design.
5. **S4 Solution Review**: Verify against `references/review-gates.md`.
6. **S5 Solution Finalization**: Update `docs/product.md` and `docs/architecture.md`.
7. **S6 Docs Source-of-Truth Scaffold & Pre-Dev UI/UX Alignment**: Populate `AGENTS.md`, `docs/README.md`, and `docs/ux.md`; for the interactive product UI/UX review, Call the Skill tool with "codex-doc-first-ui-ux-prototyping" (prototypes, layouts, component-to-API bindings, interaction states, mockups via image generation when available).
8. **S7 Docs Review**: For the link/anchor sweep, Call the Skill tool with "codex-doc-first-doc-sync" (it runs `check_docs_links.py`). If the companion skill is not installed, run the inline checklist in `references/review-gates.md`.
9. **S8 Docs Finalization & Baseline Lock**: Lock initial documentation including UI layouts and API bindings.
10. **S9 Phase Plan Breakdown**: Create `docs/delivery/phase-001.md` prioritizing shared modules.
11. **S10 Task Pack Generation**: Create `docs/delivery/tasks/TASK-001.md` with explicit contract references; for the readiness gate, Call the Skill tool with "codex-doc-first-task-pack-gate" (it runs `check_task_pack.py`). If the companion skill is not installed, run the inline checklist in `references/review-gates.md`.
12. **S11 Strategy Selection**: Select Goal, Plan, or Build mode.
13. **S12 Branch & Concurrency Setup**: Create feature branch and locks.
14. **S13 Spec-Driven Implementation**: Write code strictly complying with documented contracts & DRY rules, update `permission-audit.log` and `execution-trace.json`.
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

Two discipline-specific checkers live in companion skills (see Companion Skills & Delegation): `check_task_pack.py` in `codex-doc-first-task-pack-gate`, `check_docs_links.py` in `codex-doc-first-doc-sync`.

---

## Companion Skills & Delegation

This orchestrator stays installable and useful on its own; companion skills add depth and install independently. Delegate with the Skill tool, one skill per call:

| Step | Skill | Covers |
|---|---|---|
| S6 | `codex-doc-first-ui-ux-prototyping` | prototypes, layouts, component-to-API bindings, states, mockups |
| S7 / S18 / S20 | `codex-doc-first-doc-sync` | link/anchor validation, doc sync, writeback |
| S10 | `codex-doc-first-task-pack-gate` | Task Pack readiness gate |

If a companion skill is not installed, fall back to the inline checklist in `references/review-gates.md` and record the fallback in the Task Pack.

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
