# Pre-Dev UI/UX Alignment Gate

For graphical UI changes, align changed layouts, interactions, and states **before implementing those changes**. Reuse confirmed designs and review only affected surfaces. Backend, CLI, and script tasks without graphical UI impact skip this gate and verify their own contracts instead.

## The five alignment items

Before implementing unconfirmed graphical UI changes, resolve the applicable items; existing approvals count:

1. **Product Prototype & Navigation Flow**: overall wireframe and user journey - which screens exist and how the user moves between them.
2. **Screen UI Layout & Views**: for each core screen, the layout, component breakdown, and visual hierarchy.
3. **Bindings**: for API-backed UI, map affected components to existing service calls, inputs, outputs, and feedback states. Local-only UI records events, state, and outcomes; no API module or field projection is required.
4. **Interaction States**: loading spinners, empty states, error banners, optimistic updates - defined per view.
5. **Mockups**: when visual decisions need alignment, use available image generation and embed the result in the owning UX doc, or use wireframes/flow diagrams. Reuse approved mockups rather than generating images for unrelated changes.

## Binding matrix columns

Each row of the Component-to-API binding table (kept in `docs/ux.md`):

| Column | Meaning |
|---|---|
| Component | the view component emitting the interaction |
| API module | the centralized client/service function (never a raw fetch at the call site) |
| Parameters | request inputs |
| Response fields | consumed response data; projection only when justified by actual requirements |
| Feedback states | loading / empty / error / success rendering |

## Documentation requirement

Record changed layouts, bindings, and states in the existing owning UX document (normally `docs/ux.md`) before implementation. Record architecture impacts only when they change. The gate passes when affected decisions are resolved and traceable; unchanged approved screens do not need renewed confirmation.

## Gate failure handling

If an applicable decision is unresolved, draft it in the owning UX doc and ask only about that decision. Pause dependent UI implementation; independent authorized work can continue.

For the full gate table, `docs/ux.md` structure, and image-generation rules, see `references/ux-alignment-gate.md`.
