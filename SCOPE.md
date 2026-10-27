# Scope

This repository is the set of skills and tooling that make AI-agent software development document-first, verifiable, and archivable. It is curated: ideas are welcome, and each one is judged against the bar below. Issues are for tracking changes to the skills. Questions and discussion belong in the issue tracker with the `question` label.

## The bar

An idea or feedback issue stays open only if it clears **both** parts:

1. **Observed failure.** It describes something that went wrong in a real session: what you ran, what the skill did, what you expected. A hypothetical improvement ("it would be better if...") does not clear this part.
2. **Fits the philosophy.** It does not match anything in [`.out-of-scope/`](./.out-of-scope/) or a past rejection, and it is not a config option, a harness-specific branch, or a tweak to suit one person's workflow. Those belong in your own `CLAUDE.md` / `AGENTS.md`, or in a fork (the skills are plain files; copy them).

Size is irrelevant: a one-word fix and a rewrite face the same bar. Reactions and +1 comments do not count towards it.

The philosophy, in three rules the whole repository is built on:

- **Docs are the single source of truth.** Code never runs ahead of documentation; every architectural, API, or UI change writes back to `docs/` in the same step.
- **Fail-close.** Any missing, empty, or corrupted governance input must produce a non-zero exit code or an explicit recovery instruction. Silence is never approval.
- **Evidence over assertion.** Verification means executable gates (Merkle chain, Task Pack checks, link checks) with deterministic exit codes, not prose promises.

## By bucket

- **`codex-doc-first-development/`** (main orchestrator skill): the bar above.
- **Internal modules** (startup, doc sync, Task Pack, UI/UX): the same bar; they ship inside the main skill rather than as separate installations.
- **`.out-of-scope/`**: rejected concepts, frozen. Every entry records what was rejected and why. Read them before filing.

## Non-goals

This repository deliberately does not provide:

- a background scheduler, daemon, or persistent lock service (locks are advisory file locks used during active sessions)
- a CI provider, GitHub/GitLab integration, or automatic merge system (the methodology consumes whatever the host project has)
- pip/npm packaging of the skills (distribution is by directory copy or skill installer; `pyproject.toml` is metadata and tool configuration only)
- translations of the skill internals (English inside the skills; Chinese for `README.md` and `docs/user-guide.md` by project convention)

## Unclear issues

An issue that can't be judged against the bar gets one round of questions and the `needs-info` label. With no reply from the reporter in 14 days, it is closed. Rejections close as "not planned".
