# Doc-First Doc Sync

Documentation is the single source of truth. This guidance is the reusable discipline behind S7 (Docs Review), S18 (Change Classification & Synchronous Doc Sync), and S20 (Knowledge & Doc Writeback) of the doc-first lifecycle. Consult it whenever a change touches facts that documents own.

## The sync rule

When user feedback, a technical discovery, or an implementation change alters architecture, API contracts, UI layouts, or requirements, update the corresponding document **in the same step as, or before, the code change**:

- `docs/architecture.md` - module boundaries, service/client layers, data flow
- `docs/api.md` - endpoints, signatures, field projections
- `docs/ux.md` - screen layouts, component-to-API bindings, interaction states
- `docs/requirements.md` - scope, non-goals, success criteria
- `docs/delivery/tasks/TASK-*.md` - contracts and acceptance criteria for the active pack

Code must never run ahead of documentation. If implementation reveals a new fact, write it back to the owning document, not to a comment or a commit message.

## Change classification

| Class | Trigger | Required doc action |
|---|---|---|
| Micro | Typo, comment, internal rename with no contract change | None |
| Standard | Behavior-preserving refactor inside documented contracts | Update only changed documented facts; no doc edit if facts remain unchanged |
| Strict | Architecture, API contract, UI layout, or requirement change | Update docs **before** code; acceptance gate (S16) blocks divergence |

## Writeback checklist (S20)

At phase end, sync final facts back:

1. Reusable patterns and failure lessons as pain-point card candidates for the orchestrator's card repository (owned by the main skill).
2. Verified commands and stack facts into `AGENTS.md`.
3. Phase outcome into the phase plan and `docs/README.md` index.
4. Archive pointers into `docs/archive/`.

## Link and anchor validation

Run the checker over the docs tree before finalizing:

```bash
python <skill-root>/scripts/check_docs_links.py <project-root>/docs --json
```

Exit 0 means all relative links and heading anchors resolve. Anchors follow GitHub (GFM) rules: lowercase, punctuation dropped, **underscores kept**, each space becomes one hyphen (consecutive spaces stay consecutive hyphens). The checker enforces exactly these rules - if it passes locally, GitHub renders the same anchors.

Exit 2 means the path itself was unreadable; exit 1 lists every broken link with file, line, and target.
Here `<skill-root>` is the main skill installation directory. Check the affected tree or existing record; Quick work does not require creating `docs/`. Report the failed check, affected work, and smallest repair; a link check does not verify code contracts or tests.

## Manual fallback

If the bundled script cannot run, report the dependency or installation problem. Manual inspection can identify links to repair, but cannot be reported as an executed gate: every `[text](path.md#anchor)` must resolve and follow the documented GFM rules.

For the full distilled checklist (ownership map, S18 triggers, S20 writeback list, Docs Review gate), see `references/doc-sync-checklist.md`.
