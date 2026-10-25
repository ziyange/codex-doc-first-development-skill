---
name: codex-doc-first-start
description: Start a document-first development session: reflect on the raw idea, confirm scope and workflow mode, then run the full S0-S22 lifecycle.
disable-model-invocation: true
---

# Doc-First Start

The human entry point into the doc-first development workflow. Only you can start it; the agent cannot invoke it on its own.

## What this does

1. **Capture the idea**: paste the project idea, feature, bug, or refactoring goal.
2. **Confirm the frame**: the agent reflects on the idea (missing facts, codebase conflicts, feasibility bottlenecks), then confirms with you:
   - workflow mode: Goal, Plan, or Build
   - risk tier: Quick, Standard, or Strict
   - authorization scope: file writes, branches, subagents, GitHub/PR/CI
3. **Hand off to the lifecycle**: once the frame is confirmed, the agent runs the full S0-S22 document-first workflow.

## Usage

```text
/codex-doc-first-start

Project idea:
<<<paste your idea or requirement>>>

Authorization:
- File writes: yes/no
- Git branches: yes/no
- Subagents: yes/no
- GitHub/PR/CI: yes/no
```

## Handoff

After the frame is confirmed, this skill delegates to the orchestrator: **Call the Skill tool with "codex-doc-first-development"**. From there, the main workflow guide takes over (S0 handshake through S22 archive), delegating discipline steps to the companion skills (`codex-doc-first-doc-sync`, `codex-doc-first-task-pack-gate`, `codex-doc-first-ui-ux-prototyping`) as the lifecycle requires.
