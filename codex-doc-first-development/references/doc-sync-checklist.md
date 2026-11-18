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

Write changed facts to the owning docs (targeted patches, not rewrites):

- requirement status
- architecture and module changes
- UI mockups, interaction changes, API bindings
- new commands
- test strategy changes
- decisions and known limitations

Keep phase acceptance in the existing plan or linked task records. Add archive
pointers only for a required or useful handoff.

## Docs Review gate (S7)

Apply these checks to existing affected docs during the relevant review pass.
Use [Adaptive Workflow](adaptive-workflow.md) to select records and gates.

- Changed facts have a clear owner and match the requirements and acceptance criteria.
- Changed graphical designs and applicable API bindings are in the owning UX doc.
- Existing indexes and affected Markdown links and anchors still resolve.

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
