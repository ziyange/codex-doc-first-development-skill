# Doc-First Doc Sync

Documentation is the single source of truth. This guidance is the reusable discipline behind S7 (Docs Review), S18 (Change Classification & Synchronous Doc Sync), and S20 (Knowledge & Doc Writeback) of the doc-first lifecycle. Consult it whenever a change touches facts that documents own.

## The sync rule

When user feedback, a technical discovery, or an implementation change alters architecture, API contracts, UI layouts, or requirements, update the corresponding document **in the same step as, or before, the code change**:

- `docs/architecture.md` - module boundaries, service/client layers, data flow
- `docs/api.md` - endpoints, signatures, field projections
- `docs/ux.md` - screen layouts, component-to-API bindings, interaction states
- `docs/requirements.md` - scope, non-goals, success criteria
- Active task record - changed scope and acceptance criteria, with pointers to governing contracts

Code must never run ahead of documentation. If implementation reveals a new fact, write it back to the owning document, not to a comment or a commit message.

## Change classification

| Class | Trigger | Required doc action |
|---|---|---|
| Micro | Typo, comment, internal rename with no contract change | None |
| Standard | Behavior-preserving refactor inside documented contracts | Update only changed documented facts; no doc edit if facts remain unchanged |
| Strict | Architecture, API contract, UI layout, or requirement change | Update docs **before** code; acceptance gate (S16) blocks divergence |

## Writeback checklist (S20)

Update only facts that changed. Keep the acceptance result in the existing task
record; a phase plan, index, or archive may link to it when useful. Document new
verified project commands in the owning docs; do not copy routine check output.

## Link and anchor validation

When changing Markdown links or anchors, or when the project requires it, run the checker against the affected path:

```bash
python <skill-root>/scripts/check_docs_links.py <project-root>/docs --json
```

Exit 0 means all relative links and heading anchors resolve. Anchors follow GitHub (GFM) rules: lowercase, punctuation dropped, **underscores kept**, each space becomes one hyphen (consecutive spaces stay consecutive hyphens). The checker enforces exactly these rules - if it passes locally, GitHub renders the same anchors.

Exit 2 means the path itself was unreadable; exit 1 lists every broken link with file, line, and target.
Here `<skill-root>` is the main skill installation directory. Check the affected tree or existing record; Quick work does not require creating `docs/`. Report the failed check, affected work, and smallest repair; a link check does not verify code contracts or tests.

## Manual fallback

If the bundled script cannot run, report the dependency or installation problem. Manual inspection can identify links to repair, but cannot be reported as an executed gate: every `[text](path.md#anchor)` must resolve and follow the documented GFM rules.

For the full distilled checklist (ownership map, S18 triggers, S20 writeback list, Docs Review gate), see `references/doc-sync-checklist.md`.
