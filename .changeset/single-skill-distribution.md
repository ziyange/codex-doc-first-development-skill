---
"codex-doc-first-development-skill": major
---

Consolidate distribution into the single codex-doc-first-development directory.
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
