---
name: codex-doc-first-development
description: Document-first Codex software development workflow for turning raw software ideas or existing repository changes into requirements, docs source of truth, phase plans, Task Packs, agent delegation plans, TDD/CI validation, PR/merge gates, and archive records. Use when the user asks to start a software project from an idea, formalize a Codex or AI development methodology, generate AGENTS.md/docs/Task Packs, plan multi-agent Codex work, or run document-first development for new projects, features, bug fixes, refactors, or long-lived engineering work.
---

# Codex Doc-First Development

Use this skill to run a Codex-specific, document-first software development process from idea intake through implementation, validation, merge preparation, and archival.

## Operating Model

Treat this skill as the main engineering workflow controller for Codex. Use it to convert vague intent into durable project facts, then into bounded tasks, then into verified code changes.

Keep three layers separate:

- Product facts: user, problem, scenarios, scope, non-goals, success criteria.
- Engineering facts: architecture, contracts, commands, tests, risks, branch strategy.
- Execution facts: phase plan, Task Packs, allowed files, verification evidence, acceptance, archive.

Never let execution facts replace product or engineering facts. If implementation reveals a new fact, write it back to the correct document.

## Core Rules

- Choose the workflow mode before creating docs or editing code: quick, standard, or strict.
- Read existing repository context before proposing architecture or changing files.
- Treat docs as the project source of truth, but only create documents that reduce ambiguity or future maintenance cost.
- Track current-phase requirements with `REQ-*` IDs and testable acceptance criteria.
- Do not let a worker subagent modify code without a Task Pack.
- Create subagents only when the user explicitly authorizes parallel agent work and file ownership does not overlap.
- Use diff, test output, CI, screenshots, logs, or other inspectable evidence for acceptance; do not accept an agent's self-report as the only proof.
- Ask for explicit confirmation before merging to the main branch, force pushing, deleting, resetting history, publishing production releases, or touching secrets.
- Stop and output `BLOCKED` when requirements conflict, verification is unstable, permissions are missing, or the main Codex agent cannot judge correctness reliably.

## Workflow Selection

Start every engagement by reporting:

```text
Workflow mode:
Repository state:
Current authorization:
Must-confirm questions:
Reasonable assumptions:
Recommended first artifacts:
Next action:
```

## Workflow Modes

| Mode | Use For | Required Artifacts | Verification |
|---|---|---|---|
| Quick | Small copy changes, trivial bugs, single-file low-risk edits | Brief task note or existing issue | Most relevant command or manual check |
| Standard | Normal features, localized cross-module changes, meaningful bug fixes | Minimal docs source of truth + phase plan + Task Pack | Relevant lint/test/build/typecheck |
| Strict | New projects, architecture changes, security/payment/data migration, multi-agent development | Full docs source of truth + review gates + phase archive | TDD, local validation, CI or equivalent evidence |

Upgrade to strict mode when changes affect architecture, data models, security, permissions, billing, deployment, public APIs, or concurrent workstreams.

## Main Workflow

1. Intake and authorize.
   - Capture the user idea, target outcome, repo status, allowed operations, and high-risk boundaries.
   - Separate must-confirm questions from reasonable assumptions and later refinements.

2. Scan context.
   - For existing repos, inspect README, docs, `AGENTS.md`, package/build/test configs, CI, tests, architecture entry points, and git status.
   - For new projects, identify product type, target platform, stack constraints, deployment assumptions, and test approach.

3. Produce a formal plan.
   - Define goal, non-goals, users, scenarios, requirements, architecture, data/interface/UI implications, branch strategy, agent strategy, validation strategy, risks, rollback, and phases.
   - In strict mode, review the formal plan before creating the final docs.

4. Establish the docs source of truth.
   - Prefer the standard structure unless the task is quick or strict.
   - Create `AGENTS.md` for Codex-facing rules and `docs/README.md` as the docs entry point.
   - Keep optional docs such as `api.md`, `data-model.md`, `security.md`, `ux.md`, and `operations.md` only when they have real content.

5. Create the phase plan and Task Packs.
   - Put phase work in `docs/delivery/phase-001.md`.
   - Put each task in `docs/delivery/tasks/TASK-001.md`.
   - Every Task Pack must list requirement IDs, objective, must-read context, allowed files, forbidden files, test requirements, acceptance criteria, and expected output.

6. Choose execution strategy.
   - Use single-agent execution for tightly coupled or urgent critical-path work.
   - Use `explorer` subagents for independent read-only questions.
   - Use `worker` subagents for bounded implementation with disjoint write scopes.
   - Keep shared files and integration decisions under the main Codex agent.

7. Implement with test-first discipline.
   - Add or update tests before implementation when practical.
   - If no test harness exists, create the smallest reasonable verification path.
   - Make small scoped edits, follow existing patterns, and avoid unrelated refactors.

8. Review test quality and validate.
   - Check that tests cover acceptance criteria and have meaningful assertions.
   - Run the closest relevant commands first; broaden to lint/test/typecheck/build or CI as risk increases.
   - Record skipped or failed checks with reasons.

9. Accept, write back, and archive.
   - Return `PASS`, `REQUEST_CHANGES`, or `BLOCKED`.
   - Update docs only where the implementation changed project facts.
   - Prepare PR/merge notes only after validation evidence is available.
   - Archive phase summary, verification evidence, decisions, changes, risks, and next-step recommendations.

For the full S0-S22 lifecycle, read `references/methodology.md`.

## Docs Structure

Use these defaults and trim or expand by mode:

```text
AGENTS.md
docs/
  README.md
  product.md
  requirements.md
  architecture.md
  decisions/
  delivery/
    roadmap.md
    phase-001.md
    tasks/
      TASK-001.md
  verification/
    test-strategy.md
    reports/
  archive/
```

Quick mode may use only `AGENTS.md`, `docs/README.md`, `docs/requirements.md`, and one task file. Strict mode may add `api.md`, `data-model.md`, `security.md`, `ux.md`, `operations.md`, `docs/delivery/locks.yml`, and `docs/verification/quality-gate.md`.

## Scripted Helpers

Use scripts when the user asks to scaffold or check docs.

- `scripts/scaffold_docs.py`: create the mode-specific `AGENTS.md` and `docs/` skeleton with useful templates.
- `scripts/check_task_pack.py`: check whether a Task Pack contains required headings and basic `REQ-*` / `TASK-*` identifiers.

Run scripts with explicit paths, for example:

```bash
python scripts/scaffold_docs.py --root <project-root> --mode standard --phase 001
python scripts/check_task_pack.py <project-root>/docs/delivery/tasks/TASK-001.md
```

## Agent Delegation

Before spawning subagents, output the intended delegation plan:

```text
Agent type:
Task:
Reads:
Allowed files:
Forbidden files:
Acceptance criteria:
How the main Codex agent will review:
```

Worker prompt rules:

- Tell workers they are not alone in the codebase.
- Tell workers not to revert, overwrite, or tidy unrelated changes.
- Limit each worker to one task and one write scope.
- Require changed files, implementation summary, test commands/results, unfinished items, and risks in the final response.
- Close completed subagents after their results are reviewed.

For deeper coordination rules, branch patterns, locks, CI, PR, and conflict handling, read `references/agent-git-ci.md`.

## Status Outputs

Use these final task statuses:

- `PASS`: acceptance criteria are met and verification evidence is sufficient.
- `REQUEST_CHANGES`: defects are specific and fixable within the current task.
- `BLOCKED`: requirements, permissions, environment, CI stability, conflicts, or risk prevent reliable completion.

## References

Load these files only when needed:

- `references/methodology.md`: full S0-S22 lifecycle, artifact gates, and mode-specific behavior.
- `references/templates.md`: doc structures and artifact templates for AGENTS.md, requirements, architecture, phase plans, Task Packs, locks, verification reports, PRs, and archives.
- `references/prompts.md`: reusable prompts for startup, docs generation, phase planning, subagent delegation, worker execution, acceptance, and change control.
- `references/review-gates.md`: mode selection, formal-solution review, docs review, test quality checks, validation levels, acceptance gates, merge gates, and blocked conditions.
- `references/agent-git-ci.md`: subagent orchestration, file ownership, branch strategy, lock protocol, Git conflict handling, PR preparation, and CI evidence.
- `references/examples.md`: concrete usage patterns for a new project, feature, bug fix, refactor, docs recovery, and multi-agent phase.
