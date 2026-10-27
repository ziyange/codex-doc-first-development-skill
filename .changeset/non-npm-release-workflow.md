---
"codex-doc-first-development-skill": patch
---

Replace the npm-only Changesets action with a Python changeset planner for this
directory-distributed skill repository. Validate inputs before writes, select the
highest pending semantic bump, synchronize release metadata and changelog, and
consume changesets only in the generated version PR. Validate the generated branch
and explicitly dispatch three-platform CI for bot-created PRs. Keep tag publication
separate and preserve human review before merging. Add fixture-driven release tests.
