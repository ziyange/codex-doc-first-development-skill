# Skill Invocation Model

This repository distributes exactly one skill: `codex-doc-first-development`.
It is model-invoked (available to both model and user). Keep automatic discovery
enabled: omit `disable-model-invocation` and any explicit-only policy.

Users start it with `$codex-doc-first-development` plus a task. The model can select
the same skill for relevant document-first work. There is no separately installed
startup skill and no recursive handoff to the main entrypoint.

## Internal Modules

`references/session-start.md`, `references/doc-sync.md`, `references/task-pack.md`,
and `references/ui-ux-prototyping.md` are supporting documents, not skills. Read the
relevant file directly; run bundled helpers from the owning `scripts/` directory.
All required references, scripts, and schemas must remain within the single
installable directory. Do not use the Skill tool to load internal modules.

The main `agents/openai.yaml` owns UI metadata. Its short_description remains a
25-64 character verb phrase without a trailing period. Preserve the same invocation
policy across supported harnesses. Tests enforce the single installable entrypoint,
metadata, internal references, and isolated one-directory execution of the gates.

If another external skill is actually needed, use `Call the Skill tool with "<name>"`
for that external capability, one skill per call. No such dependency is required
for this skill's startup, doc sync, Task Pack, or graphical UI alignment guidance.
