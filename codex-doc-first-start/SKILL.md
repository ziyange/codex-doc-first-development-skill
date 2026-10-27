---
name: codex-doc-first-start
description: Start document-first development with a workflow matched to task risk and existing project context.
disable-model-invocation: true
---

# Doc-First Start

The human entry point into the doc-first development workflow. Only you can start it; the agent cannot invoke it on its own.

## What this does

1. **Capture the idea**: paste the project idea, feature, bug, or refactoring goal.
2. **Establish the frame**: the agent inspects existing docs/code and authorization, then briefly states:
   - workflow mode: Goal, Plan, or Build
   - risk tier: Quick, Standard, or Strict
   - authorization scope: file writes, branches, subagents, GitHub/PR/CI
3. **Run applicable stages**: Quick reuses an existing task/doc or one brief record; Standard maintains affected docs and a Task Pack; Strict retains full applicable governance. Existing runtime protocols keep their required inputs. Ask only about material missing choices or authorization; skip visual UX gates for non-UI work.

## Usage

```text
/codex-doc-first-start

Project idea:
<<<paste your idea or requirement>>>

Optional constraints or additional authorization (existing authorization is reused):
- File writes: yes/no
- Git branches: yes/no
- Subagents: yes/no
- GitHub/PR/CI: yes/no
```

## Handoff

After resolving material missing decisions, Call the Skill tool with "codex-doc-first-development". Follow its adaptive applicability policy and delegate only relevant discipline steps. The user can start with a natural-language task; the authorization template is optional and does not reset prior approvals.
