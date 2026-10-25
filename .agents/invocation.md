# Skill Invocation Model

Every `SKILL.md` in this repository is a skill. The one axis that splits them is **invocation** - who can reach them:

- **User-invoked**: reachable **only by the human typing its name**. These are entry points and orchestrators. Set `disable-model-invocation: true` in the frontmatter (Claude Code) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex). The `description` is **human-facing**: a one-line summary read by a person browsing slash-commands. Strip trigger lists ("Use when the user says...").
- **Model-invoked**: reachable by **model or user**. The default. Omit `disable-model-invocation` and the `policy` block from `agents/openai.yaml`. The `description` is **model-facing** and keeps rich trigger phrasing ("Use when..., mentions..., asks for...") so auto-invocation fires. The test for whether a skill should stay model-invoked: *could the model usefully reach for this autonomously?*

Each harness excludes a user-invoked skill from the model's reach in its own way, so nothing but the human can fire it: no other skill can. A user-invoked skill may invoke model-invoked skills, but it can never reach another user-invoked skill.

Every skill also carries an `agents/openai.yaml` beside its `SKILL.md`, holding `interface.display_name` and `interface.short_description` (a short verb phrase, 25-64 characters, no trailing period) for the skill picker, plus `policy.allow_implicit_invocation: false` for user-invoked skills. Keep the two harnesses in sync: a skill is user-invoked in both or neither.

## Registry

| Skill | Axis | Description style |
|---|---|---|
| `codex-doc-first-development` | model-invoked | rich triggers ("Use when starting software projects...") |
| `codex-doc-first-doc-sync` | model-invoked | rich triggers |
| `codex-doc-first-task-pack-gate` | model-invoked | rich triggers |
| `codex-doc-first-ui-ux-prototyping` | model-invoked | rich triggers |
| `codex-doc-first-start` | **user-invoked** | human-facing one-liner |

## Dependencies between skills

Dependencies are expressed as an explicit instruction to **call the Skill tool** with the named skill (`Call the Skill tool with "codex-doc-first-doc-sync"`), not deep `../other-skill/FILE.md` cross-references, and not a bare `/skill`-style mention left for the model to interpret. Naming the tool is what gets it fired. Dropping the leading `/` keeps the syntax harness-neutral.

The Skill tool takes one skill per call. A step that needs two skills is two calls, not one call with two names: say so (`Call the Skill tool twice, for "A" and "B"`), not "call it with A and B."

This convention only holds when the named skill is **model-invoked**. A user-invoked skill can never be reached this way. When a step's precondition is a user-invoked skill, phrase it as an instruction for the human to act on: "tell the user to run `/codex-doc-first-start`", never as a Skill tool call.

## Passive vs active domain work

Merely *reading* `GLOSSARY.md` for vocabulary is a one-line prose pointer, not a skill invocation. Only the active build/sharpen discipline (challenge terms, write ADRs, update `GLOSSARY.md` inline) counts as domain work.
