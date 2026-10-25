# UX Alignment Gate Reference

Distilled from S6 (Docs Source-of-Truth Creation and Pre-Dev UX Alignment) and the Pre-Dev Product UI/UX & API Alignment Gate. Use with the main `codex-doc-first-development` orchestrator; this file is the detail behind its S6 delegation step.

## Gate table

| Check item | Pass criterion | Action if failed |
|---|---|---|
| Product prototype & flow | Wireframes and screen navigation paths confirmed by the user | Re-align on page hierarchy and user flow |
| Screen UI layouts | Component breakdown, form controls, responsive layouts defined for all core screens | Draft layouts in `docs/ux.md` and confirm |
| UI-to-API binding table | Every UI trigger/component mapped to its centralized API module, parameters, projected fields, feedback states | Complete the binding matrix in `docs/ux.md` |
| Multimodal UI preview | If `generate_image` (or multimodal generation) is available, high-fidelity mockups embedded in `docs/ux.md` | Invoke `generate_image`, or fall back to ASCII wireframes + Mermaid flows |
| Full documentation | All agreed layouts, bindings, states recorded in `docs/ux.md` and `docs/architecture.md` | Write specs into `docs/` before S9 |

## `docs/ux.md` structure

1. Screen inventory and navigation flow (Mermaid).
2. Per-screen layout sections with component breakdown.
3. Component-to-API binding matrix (one table per screen or one global table).
4. Interaction state definitions: loading, empty, error, success, optimistic.
5. Embedded mockups: `![Screen Name UI Mockup](artifacts/ux/screen-name.png)`.

## Image generation rules

- Generate mockups for **core screens first**; secondary screens may follow after user confirmation.
- Save images under a stable artifacts path and reference them relatively from `docs/ux.md` so the docs stay portable.
- Mockups are alignment aids, not final design specs: once the user confirms, the binding matrix and layouts in `docs/ux.md` are the contract that S13 implements against.
- No image tool available: structured ASCII wireframes plus Mermaid UI flow diagrams are the accepted fallback.

## Handoff to planning

When the gate passes, S9 phase planning may begin. Task Packs generated afterwards reference the confirmed `docs/ux.md` sections through their Must Read anchors; any later UI change routes through the doc-sync discipline (S18) instead of silent divergence.
