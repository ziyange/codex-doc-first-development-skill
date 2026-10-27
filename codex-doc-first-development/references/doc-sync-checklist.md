# Doc Sync Checklist

Distilled from the doc-first lifecycle stages S7, S18, S20 and the Docs Review gate. Use with the main `codex-doc-first-development` orchestrator; this file is the detail behind its delegation steps.

## Ownership map

| Document | Owns |
|---|---|
| `docs/requirements.md` | scope, non-goals, success criteria, REQ-* IDs |
| `docs/architecture.md` | module boundaries, service/client layers, data flow, ADR-style decisions |
| `docs/api.md` | endpoints, signatures, field projections (`fields`), response schemas |
| `docs/ux.md` | screen layouts, wireframes, component-to-API binding matrices, interaction states, mockup images |
| `docs/delivery/phase-*.md` | phase scope, task order, dependencies |
| `docs/delivery/tasks/TASK-*.md` | objective, Allowed Files, contracts, acceptance criteria |
| `AGENTS.md` | verified commands, stack facts, agent collaboration rules |

## S18 sync triggers

Update docs in the same step as (or before) the code change when any of these change:

- functional architecture or module boundaries
- API signatures, routes, or query/response schemas
- screen UI layouts, component structures, or visual mockups
- UI-to-API interaction bindings or state transitions
- requirement scope or non-goals

Strict-class changes require appropriate risk checks and doc sync. Reuse existing authorization; pause dependent work only for unresolved scope, authority, or design decisions. A behavior-preserving internal refactor needs no doc edit when documented facts remain unchanged.

## S20 writeback list

At phase end, write back (targeted patches, not rewrites):

- requirement status
- architecture and module changes
- UI mockups, interaction changes, API bindings
- new commands
- test strategy changes
- decisions and known limitations
- phase acceptance and change records
- archive pointers into `docs/archive/`

## Docs Review gate (S7)

Docs are ready when:

Apply this checklist to existing affected docs. Quick work can reuse a task/doc or brief; no empty docs tree is required. UI bullets apply only to changed graphical UI, and API bindings only to API-backed UI.

- `docs/README.md` points to active requirements, phase, tasks, verification, and archive
- current requirements carry `REQ-*` IDs
- UI/UX mockups and Component-to-API binding matrices are fully in `docs/ux.md`
- acceptance criteria are testable
- the phase plan names tasks and dependencies, shared infrastructure first
- each Task Pack has allowed/forbidden files and explicit Must-Read contract anchors
- test strategy and expected commands are explicit
- all relative Markdown links and anchors resolve (`check_docs_links.py`, exit 0)

## Link checker rules (GFM)

The checker mirrors GitHub's slugger:

1. strip HTML tags, lowercase
2. drop punctuation - word characters, whitespace, hyphens survive; **underscores are kept**
3. each whitespace char becomes one hyphen; consecutive spaces stay consecutive hyphens

Worked examples:

- `Card 1: CONCURRENCY_RACE` -> `#card-1-concurrency_race`
- `Matching & Confidence Rules` -> `#matching--confidence-rules`
- `S10 Context Pack / Task Pack Generation` -> `#s10-context-pack--task-pack-generation`
- `1. Introduction` -> `#1-introduction`

Code blocks and inline code are masked before scanning, so syntax examples never produce false positives.
