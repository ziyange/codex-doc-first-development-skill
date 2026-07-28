# Changelog

All notable changes to the `codex-doc-first-development` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- **`scripts/check_task_pack.py`**: Upgraded to dynamically load schemas from `references/schemas.md`, enforce `MAX_ITERATIONS` ($1 \le N \le 10$), calculate weighted pain-point confidence with Top-1 exclusivity gate, reject broad wildcards, and maintain legacy v1.x fallback.
- **`SKILL.md`**: Updated to v2.0.0 specifications, integrating orthogonal autonomy modes, CoT Intake Reflection pain-point matching, dynamic permission handshake, and Exit 0-6 response protocols.
- **`references/methodology.md`**: Integrated S0 permission handshake, S1 pain-point matching, S15 3-tier validation (intent, multi-target, autonomous loop), and S20 optional DFX knowledge writeback.
- **`references/review-gates.md`**: Updated with `MAX_ITERATIONS` circuit breaker, Exit Code 0-6 table, short-circuit rules, and exhaustive 8-row dispatch lookup table.
- **`references/templates.md`**: Added `Permission & Action Plan` and `Pain-Point Card` templates.

### Deprecated
- **v1.x Legacy Task Pack Format**: Task packs lacking `MAX_ITERATIONS` or `Matched Risk Cards` issue deprecation warnings while remaining parseable in backwards compatibility mode.

---

## [1.0.0] - 2026-06-01

- Initial release of Codex Doc-First Development Skill featuring document-first development lifecycle (S0-S22), Quick/Standard/Strict workflow modes, `scaffold_docs.py`, `check_task_pack.py`, and `check_docs_links.py`.
