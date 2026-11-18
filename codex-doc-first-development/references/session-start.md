# Doc-First Start

Start through the single main skill, explicitly or through normal automatic selection. This reference provides intake guidance; it is not a separate installable entry point.

## What this does

1. **Capture the idea**: paste the project idea, feature, bug, or refactoring goal.
2. **Establish the frame**: the agent inspects existing docs/code and authorization, then briefly states:
   - risk tier: Quick, Standard, or Strict
   - authorization scope: file writes, branches, subagents, GitHub/PR/CI
   - acceptance criteria and proposed checks
3. **Run applicable stages**: use [Adaptive Workflow](adaptive-workflow.md) to choose one closure record and the relevant checks. If an audit protocol already applies, preserve its inputs. Ask only about material missing choices or authorization.

## Usage

```text
$codex-doc-first-development

Project idea:
<<<paste your idea or requirement>>>

Optional constraints or additional authorization (existing authorization is reused):
- File writes: yes/no
- Git branches: yes/no
- Subagents: yes/no
- GitHub/PR/CI: yes/no
```

## Continue the Workflow

After resolving material missing decisions, continue the main skill's applicable stages and read its internal references as needed. Do not invoke the skill recursively. The user can start with a natural-language task; the authorization template is optional and does not reset prior approvals.
