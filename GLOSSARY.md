# Glossary

Shared vocabulary for the doc-first development skills. Skills and scripts use these terms with the meanings below; anything marked *Avoid* is deprecated or ambiguous. When a skill and this glossary disagree, the glossary wins and the skill is a bug.

## Language

**Task Pack**:
A bounded unit of agent work (`TASK-###.md`) declaring objective, allowed files, contracts, test requirements, and acceptance criteria. Records execution scope for Standard/Strict work and selected runtime protocols; structural validation does not grant user authorization. Other Quick work can reuse an existing task/doc or brief.
*Avoid*: ticket, work item, spec (a spec lives in `docs/`; a Task Pack references it).

**Allowed Files**:
The explicit, narrow file-pattern whitelist inside a Task Pack's `Allowed Files` section. Broad globs (`*`, `**`, `.`) are rejected by the gate.
*Avoid*: scope, permissions (use "Allowed Files" verbatim).

**Merkle chain**:
The SHA-256 hash chain over `permission-audit.log` entries: `intent_hash = SHA256(prev_hash + ":" + action_type + ":" + normalized_path + ":" + tx_id)`. Tampering with any record breaks every downstream hash.
*Avoid*: hash log, audit chain.

**Intent**:
A recorded authorization to act (an AuditLog entry), which must exist before any Result trace. A Result without an Intent is a fail-close violation (`RESULT_WITHOUT_INTENT`).
*Avoid*: permission (reserved for `PERMISSION_GRANT`), approval.

**Result**:
An execution-trace entry (`execution-trace.json`) recording what an Intent actually did. Every non-`PERMISSION_GRANT` committed Intent requires exactly one Result.
*Avoid*: output, trace entry (when precision matters).

**Two-phase commit**:
The PENDING -> COMMITTED / ABORTED transaction protocol on audit entries. Status flips in place; status and timestamp are deliberately excluded from the hash so flips do not invalidate the chain.

**Expansion**:
A user-approved widening of the Allowed Files whitelist, recorded in `expansions.json` and anchored to a committed `PERMISSION_GRANT` in the audit log. At most 2 per task.
*Avoid*: exception, override.

**Fail-close**:
The rule that missing, empty, or corrupted governance input blocks the action (non-zero exit) instead of silently proceeding. The counterpart, fail-open, is a bug.

**Exit 0-6**:
The deterministic exit-code contract of `verify_runtime_trace.py`: 0 success, 1 iteration limit, 2 boundary/expansion violation, 3 schema/parse failure, 4 uncommitted transaction, 5 tamper/hash mismatch, 6 illegal transaction state.

**Pain-point card**:
One of the 6 domain risk cards in `references/pain-points.md`, matched during S1 intake by the main agent using the S(C) confidence score. Cards are agent-side knowledge; no CLI computes them.

**S(C)**:
The binary-feature-hit confidence score for pain-point card matching: `(2.0 x mandatory_hits + 1.0 x pattern_hits) / (2.0 x mandatory_total + 1.0 x pattern_total)`, with thresholds at 0.5 and 0.8.

**normalized_path**:
The path form recorded in audit/trace entries: forward slashes, leading `./` stripped, case preserved. Platform-independent by design so hashes verify identically on every OS.

**Doc sync**:
The mandatory write-back of architecture, API, UI, or requirements changes into `docs/` in the same step as (or before) the code change. Owned by the `codex-doc-first-doc-sync` skill.

## Relationships

- A **Task Pack** contains one **Allowed Files** whitelist and references REQ-### requirement IDs.
- An **Intent** (AuditLog entry) chains into the **Merkle chain** and pairs with a **Result** via **two-phase commit**.
- An **Expansion** widens a Task Pack's **Allowed Files** and must be anchored to a committed **PERMISSION_GRANT** Intent.

## Flagged ambiguities

- **"Mode" is overloaded three ways.** Autonomy modes (`goal`, `plan`, `build` - how much the agent may do unsupervised, `--mode` on the CLI) vs risk tiers (`Quick`, `Standard`, `Strict` - how heavy the ceremony is, workflow mode selection) vs the CLI's `--mode` argument values. Resolved: autonomy modes and CLI `--mode` share one vocabulary; risk tiers are only ever "Quick/Standard/Strict" and never appear as a `--mode` value.
- **"Gate" is overloaded.** Review gates (S4/S7/S14/S16 documentation-driven checks in `references/review-gates.md`) vs runtime gates (executable CLI checks with exit codes). Resolved: "review gate" and "runtime gate" are used explicitly.
- **"check" vs "verify" verbs.** Scripts named `check_*` validate static artifacts (Task Pack, docs links); `verify_runtime_trace.py` validates runtime evidence. Resolved: keep the existing script names; do not introduce new `check`/`verify` synonyms.
- **"Task Pack" vs "Context Pack".** A Context Pack is the read-only briefing material a Task Pack points to via "Must Read"; only the Task Pack authorizes work.
- **Schema versions vs skill versions.** `references/schemas/*.json` carries its own `title` field; the skill version (e.g. v2.3.0) lives in `SKILL.md` and `pyproject.toml`. They move independently.
