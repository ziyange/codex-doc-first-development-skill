# Prompt Pack

Use these prompts as starting points. Adapt them to the repository, user authorization, and workflow mode.

## Contents

- [Start From Zero](#start-from-zero)
- [Existing Repository Intake](#existing-repository-intake)
- [Formal Solution and Docs](#formal-solution)
- [Phase and Delegation](#phase-plan)
- [Worker Execution](#worker-task)
- [Acceptance and Change Control](#acceptance-review)

## Start From Zero

```text
Use $codex-doc-first-development as the main workflow.

Project idea:
<<<paste idea>>>

Authorization:
- Modify files: yes/no
- Create Git branches: yes/no
- Create subagents: yes/no
- Use GitHub/PR/CI: yes/no
- Install dependencies or use network: yes/no
- Commit changes: yes/no
- Create draft PR: yes/no

Use authorization already established by the conversation or environment. Ask only for missing choices that change direction or permit external or high-risk actions.

First:
1. Capture the product idea and requirements.
2. Choose quick, standard, or strict mode.
3. Separate must-confirm questions from reasonable assumptions.
4. Recommend the docs source-of-truth structure.
5. Draft the phase plan and task breakdown.
6. Explain whether subagents are useful.
```

## Existing Repository Intake

```text
Use $codex-doc-first-development to plan this change in the current repository.

Goal:
<<<task goal>>>

Constraints:
<<<constraints>>>

Please scan README, docs, AGENTS.md, package/build/test config, tests, CI, architecture entry points, and git status before proposing changes. Then output workflow mode, risks, docs updates needed, test strategy, branch strategy, and the first Task Pack.
```

## Formal Solution

```text
Create a formal implementation solution from the project idea and repository scan.

Required sections:
1. Background and goal
2. Current state
3. Users and scenarios
4. Scope and non-goals
5. Requirements and acceptance criteria
6. Architecture and module boundaries
7. Data, interface, UI, or workflow design
8. Test and validation strategy
9. Branch and PR strategy
10. Subagent strategy
11. Risks and rollback
12. Phase breakdown
13. Requirement traceability matrix
14. Open questions
```

## Docs Source of Truth

```text
Create or update the Codex-optimized docs source of truth.

Mode:
quick / standard / strict

Requirements:
- Create or update AGENTS.md.
- Create or update docs/README.md as the docs entry point.
- Create or update product, requirements, architecture, delivery, verification, and archive docs according to the mode.
- Give every current requirement a REQ ID.
- Make acceptance criteria verifiable.
- Do not create empty decorative documents.
- Create optional strict-mode documents only when applicable facts exist.
```

## Phase Plan

```text
Generate the current phase plan.

Include:
1. Phase goal, scope, and non-goals.
2. Related REQ IDs.
3. Task list with TASK IDs.
4. Allowed and forbidden files for each task.
5. Test requirements and acceptance criteria.
6. Parallel vs serial task classification.
7. Suggested subagents, if authorized and useful.
8. Branch strategy.
9. Archive path.
```

## Subagent Authorization Plan

```text
I allow subagents for parallel work.

Before spawning any subagent, list:
1. Agent type: explorer or worker.
2. Task.
3. Reads.
4. Allowed files.
5. Forbidden files.
6. Acceptance criteria.
7. How the main Codex agent will review results.

Only create workers for disjoint write scopes. Keep shared files under the main Codex agent.
```

## Worker Task

```text
You are a Codex worker. You are not alone in the codebase.
Do not revert, overwrite, or tidy changes unrelated to your task.

Task Pack:
<<<paste Task Pack>>>

Rules:
1. Read only the required context unless you need adjacent code to implement safely.
2. Modify only allowed files.
3. Do not modify forbidden files.
4. Do not expand scope.
5. Add or update tests according to the Task Pack.
6. Run required verification commands.
7. If requirements, interfaces, data, tests, or file ownership conflict, output BLOCKED.

Final output:
1. Changed files.
2. Implementation summary.
3. Test commands and results.
4. Unfinished items.
5. Risks.
6. Recommendation for main-agent acceptance.
```

## Acceptance Review

```text
Enter Codex main-agent acceptance mode.

Inputs:
- Task Pack
- git diff
- Subagent output, if any
- Test output
- CI/PR checks
- Docs changes

Rules:
1. Do not accept agent self-report as the only evidence.
2. Check every acceptance criterion.
3. Check whether tests have meaningful assertions.
4. Check for unrelated changes.
5. Check whether docs need writeback.
6. Output PASS, REQUEST_CHANGES, or BLOCKED.
7. Label evidence as planned, locally executed, isolated, or externally executed.
```

## Change Control

```text
Classify this new request during active development.

Change:
<<<change request>>>

Current context:
<<<phase/task/status>>>

Classify as:
- micro: does not affect architecture, interface, data, or phase plan
- standard: affects requirements, tests, or local implementation plan
- strict: affects architecture, data, security, milestone, or multiple tasks

Output impact, docs updates, task updates, agent impact, verification impact, and whether user confirmation is required.
```
