---
name: codex-doc-first-development
description: Use when planning or implementing document-first software changes, keeping changed contracts in sync with docs, and verifying work at the level its risk requires.
---

# Codex Doc-First Development (v3.1.0 Released)

Use one installed skill to turn intent into scoped, verified changes. Follow platform, user, and repository instructions. Read `references/adaptive-workflow.md` first: it selects risk, records, and checks. Treat S0–S22 as an index of available stages.

## Run the work

1. **Before editing:** Inspect the existing project and docs, establish authorized scope, and define an observable outcome and how to verify it. Reuse prior decisions. Ask only about material unknowns or missing authority.
2. **While editing:** Stay within scope. Update changed product, architecture, API, and UI facts in their owning docs before or alongside implementation. Reuse existing contracts, modules, tests, and confirmed designs.
3. **Before delivering:** Review the actual changes, verify acceptance, and put the real result and any blockers in the same task record. A check that was planned or could not run has not passed. Fix local failures and rerun affected or required checks.

Use one record per independently verifiable plan point. Quick work without an existing task record can close in the final reply. Standard and Strict reuse existing project records where possible. Strict adds checks for the actual risk; it does not activate transaction logging by itself.

## Load only the applicable guidance

| Stage | Read when needed |
|---|---|
| S0–S1: Authorization and intake | `references/session-start.md`; `references/pain-points.md` for relevant domain risks |
| **S2 Repository** scan and optional initialization | Preview `python <skill-root>/scripts/scaffold_docs.py --root <project-root> --auto-detect --dry-run` before creating docs |
| S3–S5: Solution and review | `references/methodology.md` for design stages; `references/review-gates.md` for focused review |
| S6–S8: Docs baseline | `references/doc-sync.md`; `references/ui-ux-prototyping.md` only for graphical UI changes |
| S9–S10: Phase and bounded tasks | `references/templates.md` when a record is missing; `references/task-pack.md` if a formal Task Pack applies |
| S11–S13: Execution and coordination | `references/agent-git-ci.md` when branches, parallel work, or CI require coordination |
| S14–S16: Verification and acceptance | `references/review-gates.md` for choosing evidence and resolving blockers |
| S17–S22: Conflicts, sync, integration, release, archive | `references/methodology.md` for applicable steps; reference existing evidence at handoffs |

## Script selection

- Run `scripts/check_docs_links.py` on affected Markdown when changing links or anchors or when required by the project.
- Run `scripts/check_task_pack.py` when a formal Task Pack applies. Structural validation does not grant authority or prove behavior.
- Read `references/runtime-audit.md` only when the bundled audit protocol is active. It covers `scripts/verify_runtime_trace.py`, `scripts/check_permission_log.py`, and `scripts/lock_manager.py`. Preserve configured audit inputs, scope checks, and iteration limits.
- Resolve scripts from the installed skill and artifacts from the downstream project. Report required scripts that cannot run as unverified.

`references/capabilities-matrix.md` maps all lifecycle stages. `references/examples.md` and `references/prompts.md` provide optional patterns.
