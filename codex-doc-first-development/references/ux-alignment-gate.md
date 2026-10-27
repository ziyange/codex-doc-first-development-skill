# UX Alignment Gate Reference

Distilled from S6 (Docs Source-of-Truth Creation and Pre-Dev UX Alignment) and the Pre-Dev Product UI/UX & API Alignment Gate. Use with the main `codex-doc-first-development` orchestrator; this file is the detail behind its S6 delegation step.

Apply only to changed graphical UI surfaces. Reuse approved designs and existing
UX docs; non-UI changes skip visual artifacts and validate their own contracts.
Local-only UI records events, state, and outcomes instead of API bindings.

## Gate table

| Check item | Pass criterion | Action if failed |
|---|---|---|
| Product prototype & flow | Affected flow decisions resolved; existing approvals count | Ask only about unresolved changed flow |
| Screen UI layouts | Changed components and layouts defined | Draft affected layouts in owning UX doc |
| UI-to-API binding table | Affected API bindings and feedback states mapped when API-backed | Record service calls/inputs/outputs; local UI uses events/state/outcomes |
| Multimodal UI preview | Unresolved visual decisions have a suitable proposal | Use available image tools or wireframes; reuse approved mockups |
| Full documentation | All agreed layouts, bindings, states recorded in `docs/ux.md` and `docs/architecture.md` | Write specs into `docs/` before S9 |

## `docs/ux.md` structure

1. Screen inventory and navigation flow (Mermaid).
2. Per-screen layout sections with component breakdown.
3. Component-to-API binding matrix (one table per screen or one global table).
4. Interaction state definitions: loading, empty, error, success, optimistic.
5. Embedded mockups: `![Screen Name UI Mockup](artifacts/ux/screen-name.png)`.

## Image generation rules

- Generate mockups for unresolved visual decisions on affected core screens; reuse approved mockups for unchanged designs.
- Save images under a stable artifacts path and reference them relatively from `docs/ux.md` so the docs stay portable.
- Mockups are alignment aids, not final design specs: once the user confirms, the binding matrix and layouts in `docs/ux.md` are the contract that S13 implements against.
- No image tool available: structured ASCII wireframes plus Mermaid UI flow diagrams are the accepted fallback.

## Handoff to planning

When applicable decisions are resolved, dependent UI implementation may begin. Reference the owning UX doc anchors from the applicable task record. Later UI changes route through doc sync; pause only work dependent on unresolved decisions.
