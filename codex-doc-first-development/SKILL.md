---
name: codex-doc-first-development
description: Guides Codex through document-first software development v2.1.0 with orthogonal autonomy modes (Goal/Plan/Build), domain pain-point card matching, standalone JSON schemas, executable Merkle chain runtime verification (Exit codes 0-6), advisory file lock management, and full lifecycle (S0-S22) governance. Use when starting software projects, formalizing AI development methodology, scaffolding docs, bounding multi-agent tasks, or executing verifiable software development.
---

# Codex Doc-First Development (v2.1.0 Released)

Use this skill to execute a Codex-specific, document-first software development process from idea intake through implementation, validation, merge preparation, and archival.

## Operating Model

Treat this skill as the main engineering workflow guide within higher-priority platform, user, and repository instructions. Use it to convert vague intent into durable project facts, then into bounded tasks, then into verified code changes.

Keep three layers separate:
- Product facts: user, problem, scenarios, scope, non-goals, success criteria.
- Engineering facts: architecture, contracts, commands, tests, risks, branch strategy.
- Execution facts: phase plan, Task Packs, allowed files, verification evidence, acceptance, archive.

Never let execution facts replace product or engineering facts. If implementation reveals a new fact, write it back to the correct document.

---

## Core Rules & Governance Protocols

1. **Orthogonal Autonomy Modes**:
   - **Goal Mode**: Closed whitelist, autonomous iteration up to `MAX_ITERATIONS` ($1 \le N \le 10$). Triggers circuit breaker on $k > N$.
   - **Plan Mode**: Phase-by-phase permission handshake. Single-step commit for `MODE_SWITCH`.
   - **Build Mode**: Low-overhead stream execution against blacklist patterns (`.git/*`, `permission-audit.log`, `.log.lock`, etc.).

2. **Domain Pain-Point Card Matching**:
   - During `CoT Intake Reflection`, compute binary feature hit score $S(C)$ against 6 domain cards (`references/pain-points.md`).
   - If $S(C) \ge 0.8$: High confidence match. Enforce targeted inspection checklist.
   - If $0.5 \le S(C) < 0.8$: Mid confidence match. Require `user_confirmed: true`.
   - Top-1 exclusivity gate: only activate highest scoring card $\ge 0.5$. Lower candidates logged in `ignored_candidates`.

3. **Machine-First Standalone JSON Schemas**:
   - Load JSON schemas directly from standalone files (`references/schemas/ExecutionTraceSchema.json`, `references/schemas/AuditLogSchema.json`, `references/schemas/ExpansionSchema.json`, `references/schemas/TaskPackSchema.json`, `references/schemas/PainPointCardSchema.json`), with Markdown fallback.

4. **Executable Merkle Chain Runtime Verification & Lock Manager**:
   - Run `scripts/verify_runtime_trace.py` for hard gate checks before proceeding or finalizing.
   - Computes SHA256 chain: `intent_hash_n = SHA256(prev_hash_n + ":" + action_type_n + ":" + normalized_path_n + ":" + tx_id_n)`.
   - Enforces `docs/delivery/.log.lock` single-writer file mutex locking using `lock_manager.py` with PID & timestamp stale lock cleanup.

---

## Exit Code Protocol (0–6) & Exhaustive Main-Agent Dispatch Table

Main agent SKILL.md handles non-Exit-0 CLI outputs by **strictly looking up the `(exit_code, runtime_event_reason)` tuple**:

| `exit_code` | `runtime_event_reason` | Scenario Description | Main-Agent SKILL.md Dispatch Action |
|:---:|:---:|---|---|
| `0` | `null` | AuditLog, Trace, and Merkle chain fully valid | **Pass**: Proceed with current iteration execution. |
| `1` | `null` | Iteration limit exceeded (`k > MAX_ITERATIONS`) | **Circuit-Break Halt**: Terminate autonomous self-healing, report `BLOCKED`. |
| `2` | `"EXPANSION_LIMIT_EXCEEDED"` | Expansion count exceeded limit (max 2) | **Fuse & Downgrade**: Force downgrade Goal mode to Plan mode. |
| `2` | `null` | File edit out of whitelist boundary | **Issue Expansion**: Parse `offending_files`, request user expansion approval. |
| `3` | `null` | Schema missing, file corrupt, or parse failure | **Fail-Close**: Halt immediately, prompt user to repair environment. |
| `4` | `"SAFELY_ABORTED_OPERATION"` | Lock write exception safely aborted to ABORTED | **Safe Retry**: Inform user action was safely aborted, allow action retry. |
| `4` | `null` | AuditLog contains uncommitted transaction | **Fallback Dictionary Parse**: Parse `reason_details`: for `UNCOMMITTED_PENDING` retry action or abort; for `COMMITTED_RESULT_MISSING` **write Result trace ONLY, DO NOT retry action**. |
| `5` | `null` | Merkle chain broken, hash mismatch, or trace tampered | **Security Alert (Short-circuit)**: Halt immediately, alert audit log corruption. |
| `6` | `null` | `PENDING+Present` or `ABORTED+Present` contradiction | **Data Audit (Short-circuit)**: Halt immediately, request manual audit intervention. |

---

## Workflow Modes & Risk Levels

| Mode | Risk Level | Required Artifacts | Verification Gate |
|---|---|---|---|
| Quick | Low | Task Pack or brief note | Single relevant command check |
| Standard | Medium | Minimal docs source of truth + Phase plan + Task Pack | `scripts/check_task_pack.py` + unit tests |
| Strict | High / Critical | Full docs source of truth + Merkle trace audit | `scripts/verify_runtime_trace.py --json` |

---

## Main Workflow (S0 – S22)

1. **S0 Permission & Handshake**: Establish authorization scope and initial workflow mode.
2. **S1 Intake & CoT Reflection**: Execute CoT intake analysis, compute pain-point card confidence score $S(C)$.
3. **S2 Repository Context Scan**: Run `scripts/scaffold_docs.py --auto-detect`.
4. **S3 Formal Solution Draft**: Create architecture, data model, and interface specs.
5. **S4 Solution Review**: Verify against `references/review-gates.md`.
6. **S5 Solution Finalization**: Update `docs/product.md` and `docs/architecture.md`.
7. **S6 Docs Source-of-Truth Scaffold**: Populate `AGENTS.md` and `docs/README.md`.
8. **S7 Docs Review**: Run `python scripts/check_docs_links.py docs --json`.
9. **S8 Docs Finalization**: Lock initial documentation.
10. **S9 Phase Plan Breakdown**: Create `docs/delivery/phase-001.md`.
11. **S10 Task Pack Generation**: Create `docs/delivery/tasks/TASK-001.md` and validate with `python scripts/check_task_pack.py <task-path> --json`.
12. **S11 Strategy Selection**: Select Goal, Plan, or Build mode.
13. **S12 Branch & Concurrency Setup**: Create feature branch and locks.
14. **S13 Implementation**: Write code, update `permission-audit.log` and `execution-trace.json`.
15. **S14 Test Quality Review**: Verify test coverage and meaningful assertions.
16. **S15 Runtime Gate Validation**: Execute `python scripts/verify_runtime_trace.py --mode <mode> --json`.
17. **S16 Acceptance Decision**: Inspect Exit Code (0 = PASS, 2/4 = Retry/Expand, 1/3/5/6 = HALT).
18. **S17 Git Conflict Handling**: Resolve branch merge conflicts cleanly.
19. **S18 Change Classification**: Categorize changes into docs, code, and test artifacts.
20. **S19 Phase Acceptance**: Validate phase completion against `phase-xxx.md`.
21. **S20 Knowledge Writeback**: Extract reusable patterns into `references/pain-points.md` if DFX quality gate passes.
22. **S21 Merge / PR Preparation**: Prepare PR summary with verified CLI trace outputs.
23. **S22 Phase Archive**: Archive phase outputs to `docs/archive/`.

---

## Scripted Helpers Summary

- `scripts/verify_runtime_trace.py`: Verifies runtime trace, Merkle chain, two-phase commit, and exit codes 0-6.
- `scripts/check_task_pack.py`: Validates Task Pack Markdown structure, `MAX_ITERATIONS`, allowed files, and schema compliance.
- `scripts/check_permission_log.py`: Internal module for static Merkle chain verification.
- `scripts/check_docs_links.py`: Statically validates Markdown links and anchors.
- `scripts/scaffold_docs.py`: Scaffolds mode-specific documentation directory skeletons.

---

## References

For full operational specifications, load these single-source reference documents:
- `references/schemas.md`: 4 authoritative JSON Schemas.
- `references/capabilities-matrix.md`: S0-S22 lifecycle asset mapping.
- `references/pain-points.md`: 6 domain pain-point cards.
- `references/methodology.md`: Full S0-S22 lifecycle methodology.
- `references/review-gates.md`: Full gate definitions and exit code tables.
- `references/templates.md`: Artifact templates.
- `CHANGELOG.md`: Version 2.0.0 release history.
