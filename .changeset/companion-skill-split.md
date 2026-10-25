---
"codex-doc-first-development-skill": minor
---

Split the monolithic skill into a composable suite along the invocation axis.

### Added

- `codex-doc-first-doc-sync` (model-invoked): S18/S20 doc-sync discipline plus the `check_docs_links.py` checker, moved from the main skill with its own `references/doc-sync-checklist.md`.
- `codex-doc-first-task-pack-gate` (model-invoked): Task Pack readiness gate (S9-S10) plus the `check_task_pack.py` checker, moved from the main skill with its own `references/task-pack-gate.md`.
- `codex-doc-first-ui-ux-prototyping` (model-invoked): the S6 pre-dev UI/UX alignment gate (prototypes, layouts, component-to-API binding matrix, interaction states, mockup generation) with `references/ux-alignment-gate.md`.
- `codex-doc-first-start` (**user-invoked**): human entry point that confirms the idea, frame, and authorization, then hands off to the orchestrator via the Skill tool. Declares `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.

### Changed

- The main `codex-doc-first-development` skill now delegates S6/S7/S10/S18/S20 discipline steps to the companion skills via "Call the Skill tool with ...", falling back to the inline `references/review-gates.md` checklists when a companion is not installed.
- Pain-point Card 4's inspection command is now a skill reference (its script moved to `codex-doc-first-doc-sync`).

### Breaking

- `scripts/check_docs_links.py` and `scripts/check_task_pack.py` no longer live in the main skill directory. Direct CLI callers must either install the owning companion skill and invoke the script from its directory, or rely on the main skill's documented inline fallback. Existing installations (whole-directory copies) are unaffected; new installs of the main skill remain fully functional through the fallback path.
