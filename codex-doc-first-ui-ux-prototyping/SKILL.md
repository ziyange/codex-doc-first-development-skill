---
name: codex-doc-first-ui-ux-prototyping
description: Use when aligning product UI/UX with the user before coding: screen layouts, component-to-API binding tables, interaction states, and high-fidelity mockups via image generation tools. This is the mandatory pre-dev alignment gate (S6) of the doc-first lifecycle.
---

# Pre-Dev UI/UX Alignment Gate

After requirements and API architecture are drafted and **before any code is written**, the product's UI must be aligned with the user and fully documented. This skill is the reusable discipline behind S6 of the doc-first lifecycle.

## The five alignment items

Before generating Phase Plans and Task Packs, confirm with the user:

1. **Product Prototype & Navigation Flow**: overall wireframe and user journey - which screens exist and how the user moves between them.
2. **Screen UI Layout & Views**: for each core screen, the layout, component breakdown, and visual hierarchy.
3. **Component-to-API Binding Matrix**: an explicit table mapping each UI component to its unified API module - request parameters, projected response fields (`fields`), and the UI feedback state.
4. **Interaction States**: loading spinners, empty states, error banners, optimistic updates - defined per view.
5. **Multimodal Mockups**: if the environment provides image generation (`generate_image` or multimodal generation), proactively generate high-fidelity mockups for core screens, save them as artifacts, and embed them with `![Screen Name UI Mockup](path/to/image.png)` in `docs/ux.md`. If no image tool exists, fall back to structured ASCII wireframes and Mermaid UI flow diagrams.

## Binding matrix columns

Each row of the Component-to-API binding table (kept in `docs/ux.md`):

| Column | Meaning |
|---|---|
| Component | the view component emitting the interaction |
| API module | the centralized client/service function (never a raw fetch at the call site) |
| Parameters | request inputs |
| Projected fields | the `fields` projection the view consumes |
| Feedback states | loading / empty / error / success rendering |

## Documentation requirement

All agreed prototypes, layouts, bindings, and states are recorded in `docs/ux.md` (and architecture impacts in `docs/architecture.md`) **before** S9. The gate passes when: docs entry exists, requirements trace to `REQ-*` IDs, wireframes/layouts/bindings are fully documented, and every project fact is findable from docs.

## Gate failure handling

If any item is unconfirmed, re-align with the user on that item and draft the missing piece in `docs/ux.md` - do not proceed to phase planning or coding with an open UI question.

For the full gate table, `docs/ux.md` structure, and image-generation rules, see `references/ux-alignment-gate.md`.
