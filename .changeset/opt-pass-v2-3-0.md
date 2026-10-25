---
"codex-doc-first-development-skill": minor
---

Optimization pass v2.3.0: correctness fixes, repository conventions, and companion-skill groundwork.

### Fixed
- Removed dead code (`compute_file_sha256`, `calculate_card_confidence`) and the inert `--schemas` argument of `check_task_pack.py`; documented the removed claims in CHANGELOG correction notes.
- `check_task_pack.py` now surfaces legacy-format and tautological-test findings as non-blocking `warnings` (exit codes unchanged).
- `verify_runtime_trace.py`: `--mode` restricted to goal/plan/build (fail-fast); empty Allowed Files in goal/plan mode now fails closed (Exit 2) instead of skipping boundary checks; Result traces without an AuditLog intent now yield Exit 4 (`RESULT_WITHOUT_INTENT`); `parse_task_pack` no longer treats sentence-style lines as glob patterns.
- `normalize_path` is platform-independent (case always preserved), so Merkle intent hashes verify identically on Windows, Linux, and macOS.
- `lock_manager.py`: OS lock is taken before any metadata inspection/rewrite; the lock file is never deleted on release (unlink-while-locked race); Windows lock regions for acquire/release now match; broad exception handling narrowed.
- `check_docs_links.py` slug generation now mirrors github-slugger exactly; repaired 12 genuinely broken anchors across references/ (underscores and `&` cases).
- `references/schemas.md` synchronized with the standalone JSON authority (TaskPackSchema added, `artifact_metadata` added to both degraded blocks); `references/pain-points.md` inspection commands repaired; README/user-guide claims aligned with actual behavior.

### Added
- Repository conventions: `AGENTS.md` (+ `CLAUDE.md` symlink), `SCOPE.md`, `GLOSSARY.md`, `.agents/invocation.md`, `.out-of-scope/`, changesets-based versioning, and the CHANGELOG moved to the repository root.
- Tests: GFM anchor semantics, schemas.md/JSON parity, pain-point card validity, fail-close edge cases (TC-V20..V24), and lock-manager race coverage.
