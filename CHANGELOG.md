# Changelog

All notable changes to this repository - the `codex-doc-first-development` skill, its companion skills, and the tooling around them - are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-10-27

### Changed

- Adapt lifecycle artifacts and design gates to task risk. Quick work reuses existing
  records or one brief; Standard and Strict maintain applicable contracts and gates.
  Reuse established authorization and approved designs, skip visual artifacts for
  non-UI work, and distinguish Task Pack structure from execution authority. Preserve
  selected runtime protocols, skill invocation policy, script ownership, and CLI
  exit codes/JSON interfaces. Add applicability regressions and installed command
  checks, and correct residual path examples and a Ruff line-length failure.
  
  Fix an observed fail-open runtime gate: missing required inputs and malformed
  JSON records now return existing Exit 3 rather than silently passing. Goal requires
  an explicit valid MAX_ITERATIONS. Missing optional expansions remain supported;
  malformed existing expansions fail closed. Initialized empty audit/trace states
  remain supported. No exit code or payload shape changes.
  
  Pin the three-OS test matrix to Python-3.9-compatible runner images after the
  Ubuntu latest image upgrade broke interpreter installation before tests ran.

- Resolve default runtime schemas relative to the installed skill rather than the
  downstream working directory. Preserve explicit schema overrides and fail-close
  behavior for missing schemas. Correct the S2 scaffold command, clarify S15 paths,
  remove stale CLI version text, and test downstream execution and the 150-line
  entrypoint limit. No script moves or protocol changes.

- Replace the npm-only Changesets action with a Python changeset planner for this
  directory-distributed skill repository. Validate inputs before writes, select the
  highest pending semantic bump, synchronize release metadata and changelog, and
  consume changesets only in the generated version PR. Validate the generated branch
  and explicitly dispatch three-platform CI for bot-created PRs. Keep tag publication
  separate and preserve human review before merging. Add fixture-driven release tests.

- Consolidate distribution into the single codex-doc-first-development directory.
  Move doc-sync, Task Pack, UI/UX, and startup guidance into internal references and
  bundle check_docs_links.py and check_task_pack.py in the main scripts directory.
  Remove the four companion installable entrypoints and their UI metadata. Users
  install and invoke only the main skill; no recursive Skill-tool handoffs or manual
  fallbacks for absent companion checkers remain.
  
  BREAKING: checker paths move from their former companion directories to
  codex-doc-first-development/scripts/. Update downstream CLI/CI paths and move old
  companion installations out of skill discovery directories after backing them up.
  Checker exit codes, JSON payloads, and the main skill name are unchanged. Rewrite
  README and the Chinese guide for single-directory installation, migrate CI and
  release validation, and add an isolated copied-bundle test of all three gates.

## [2.3.0] - 2026-10-25

### Added

- **Companion skills (composable suite)**: the monolithic skill is split along the invocation axis into 1 orchestrator + 4 companion skills:
  - `codex-doc-first-doc-sync` (model-invoked): S18/S20 doc-sync discipline plus `check_docs_links.py`, moved from the main skill, with `references/doc-sync-checklist.md`.
  - `codex-doc-first-task-pack-gate` (model-invoked): S9-S10 Task Pack readiness gate plus `check_task_pack.py`, moved from the main skill, with `references/task-pack-gate.md`.
  - `codex-doc-first-ui-ux-prototyping` (model-invoked): the S6 pre-dev UI/UX alignment gate with `references/ux-alignment-gate.md`.
  - `codex-doc-first-start` (**user-invoked**): human entry point declaring `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- **Repository conventions** (modeled on mattpocock/skills): `AGENTS.md` (+ `CLAUDE.md` symlink), `SCOPE.md` (contribution bar), `GLOSSARY.md` (shared vocabulary with resolved ambiguities), `.agents/invocation.md` (user-invoked vs model-invoked axis, "Call the Skill tool with ..." dependency syntax), `.out-of-scope/` (rejected concepts), changesets-based versioning, and the CHANGELOG moved to the repository root.
- **CI dogfooding and linting**: `docs-selfcheck` job runs the repo's own gates (link check, Task Pack gate, end-to-end runtime gate on fixtures); `lint` job runs ruff; test matrix slimmed to 3 OS x {3.9, 3.12}; `release.yml` adds changesets version PRs and tag-triggered GitHub Releases.
- **Tests**: GFM anchor semantics, schemas.md/JSON parity, pain-point card validity, fail-close edge cases (TC-V20~TC-V24), lock-manager race coverage, and multi-skill consistency guards (76 tests total).

### Fixed

- Removed dead code (`compute_file_sha256`, `calculate_card_confidence`) and the inert `--schemas` argument of `check_task_pack.py`; correction notes added to the 2.0.0 CHANGELOG entry.
- `check_task_pack.py` now surfaces legacy-format and tautological-test findings as non-blocking `warnings` (exit codes unchanged).
- `verify_runtime_trace.py`: `--mode` restricted to goal/plan/build (fail-fast); empty Allowed Files in goal/plan mode now fails closed (Exit 2) instead of skipping boundary checks; Result traces without an AuditLog intent now yield Exit 4 (`RESULT_WITHOUT_INTENT`); `parse_task_pack` no longer treats sentence-style lines as glob patterns.
- `normalize_path` is platform-independent (case always preserved), so Merkle intent hashes verify identically on Windows, Linux, and macOS.
- `lock_manager.py`: the OS lock is taken before any metadata inspection/rewrite; the lock file is never deleted on release (unlink-while-locked race); Windows lock regions for acquire/release now match; broad exception handling narrowed.
- `check_docs_links.py` slug generation now mirrors github-slugger exactly; repaired 12 genuinely broken anchors across references/.
- `references/schemas.md` synchronized with the standalone JSON authority (TaskPackSchema added, `artifact_metadata` added to both degraded blocks); `references/pain-points.md` inspection commands repaired; README/user-guide claims aligned with actual behavior.

### Breaking

- `scripts/check_docs_links.py` and `scripts/check_task_pack.py` no longer live in the main skill directory; they moved to `codex-doc-first-doc-sync/` and `codex-doc-first-task-pack-gate/` respectively. Direct CLI callers should install the owning companion skill and invoke the script from its directory. Existing whole-directory installations are unaffected, and a fresh main-skill-only install remains fully functional through the documented inline fallback in `references/review-gates.md`.

---

## [2.2.0] - 2026-08-24

### Added
- **Functional Independence & DRY Reusability Architecture**: Mandated centralized API client / service layers (`client.ts` / `service.py`) for all data requests and backend dynamic field projection (`fields` parameter), eliminating duplicate request logic across multiple components.
- **Pre-Dev Interactive UI/UX Design & Prototyping Gate**: Added mandatory alignment with user on product prototypes, screen UI layouts, component-to-API binding matrices, and user interaction states before coding begins.
- **Multimodal Image Generation Integration**: Added support for proactively generating high-fidelity UI visual mockups via `generate_image` and embedding them into `docs/ux.md`.
- **Strict Spec-Driven Targeted Development**: Added spec-driven execution rules ensuring code 100% conforms to documented API contracts, parameter names, and UI structures without ad-hoc drift.
- **Synchronous Two-Way Documentation Sync**: Mandated that any user feedback, architectural modification, API change, or UI interaction update must synchronously update `docs/` in lockstep with or prior to code changes.
- **Code-Doc Traceability Acceptance Gate**: Enhanced S14 (DRY Review) and S16 (Acceptance) to block PRs/commits that introduce duplicate requests, diverge from documented contracts, or lack synchronous doc updates.

---

## [2.0.0] - 2026-07-28

### Added
- **Orthogonal Autonomy Modes**: Introduced Goal Mode (closed whitelist + iteration circuit breaker), Plan Mode (phase-by-phase permission handshake), and Build Mode (low-overhead stream execution) orthogonal to Quick/Standard/Strict risk levels.
- **Single Source of Truth Schemas**: Created `references/schemas.md` containing 4 authoritative JSON Schemas (`ExecutionTraceSchema`, `AuditLogSchema`, `ExpansionSchema`, `PainPointCardSchema`) dynamically loaded via `// schema-id` anchors.
- **Executable Runtime Hard Gates**: Created `scripts/verify_runtime_trace.py` enforcing exit codes 0-6, `--next-iteration` bounds, SHA256 Merkle chain integrity, Two-Phase Commit transaction pairing, and `.log.lock` single-writer mutex locking.
- **Domain Pain-Point Cards**: Created `references/pain-points.md` featuring 6 domain risk cards (`CONCURRENCY_RACE`, `STATE_MEMORY_LEAK`, `SCHEMA_MIGRATION`, `CROSS_PLATFORM`, `PERFORMANCE_DEGRADATION`, `SECURITY_PERMISSION`) with binary 0/1 confidence scoring.
- **Capability Matrix**: Created `references/capabilities-matrix.md` mapping lifecycle stages S0-S22 to Tool, Knowledge, and Skill assets.
- **Internal Audit Helper**: Created `scripts/check_permission_log.py` as an internal module for static log verification.
- **Structured Exit Payloads**: Added `--json` structured outputs supporting `exit_code`, `reason`, `runtime_event_reason`, `reason_details`, `scan_truncated`, `offending_files`, `uncommitted_tx_ids`, and `ignored_candidates`.
- **Unit Test Benchmark Suite**: Added `tests/test_verify_runtime_trace.py` (TC-V01 ~ TC-V19) and `tests/test_check_task_pack.py` (TC-C01 ~ TC-C02).

### Changed
- **`scripts/check_task_pack.py`**: Upgraded to enforce `MAX_ITERATIONS` ($1 \le N \le 10$), reject broad wildcards, and maintain legacy v1.x fallback.
  - *Correction (v2.3.0): this entry originally also claimed dynamic schema loading from `references/schemas.md` and weighted pain-point confidence calculation with a Top-1 exclusivity gate. Neither was ever wired into the CLI (the `--schemas` argument was inert and the confidence scoring lives in the S1 main-agent reflection against `references/pain-points.md`, not in this script). The claims are removed here; the v2.3.0 release notes document the dead-code removal.*
- **`SKILL.md`**: Updated to v2.0.0 specifications, integrating orthogonal autonomy modes, CoT Intake Reflection pain-point matching, dynamic permission handshake, and Exit 0-6 response protocols.
- **`references/methodology.md`**: Integrated S0 permission handshake, S1 pain-point matching, S15 3-tier validation (intent, multi-target, autonomous loop), and S20 optional DFX knowledge writeback.
- **`references/review-gates.md`**: Updated with `MAX_ITERATIONS` circuit breaker, Exit Code 0-6 table, short-circuit rules, and exhaustive 8-row dispatch lookup table.
- **`references/templates.md`**: Added `Permission & Action Plan` and `Pain-Point Card` templates.

### Deprecated
- **v1.x Legacy Task Pack Format**: Task packs lacking `MAX_ITERATIONS` or `Matched Risk Cards` issue deprecation warnings while remaining parseable in backwards compatibility mode.

---

## [1.0.0] - 2026-06-01

- Initial release of Codex Doc-First Development Skill featuring document-first development lifecycle (S0-S22), Quick/Standard/Strict workflow modes, `scaffold_docs.py`, `check_task_pack.py`, and `check_docs_links.py`.
