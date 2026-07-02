# Codex Doc-First Development Skill

Engineering-grade document-first software development workflow for Codex.

This repository contains a reusable Codex skill that turns raw software ideas or existing repository changes into requirements, docs source of truth, phase plans, Task Packs, subagent delegation plans, validation gates, PR/merge preparation, and archive records.

## Skill

```text
codex-doc-first-development/
  SKILL.md
  agents/
    openai.yaml
  references/
    methodology.md
    templates.md
    prompts.md
    review-gates.md
    agent-git-ci.md
    examples.md
  scripts/
    scaffold_docs.py
    check_task_pack.py
```

## Install

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item `
  -LiteralPath ".\codex-doc-first-development" `
  -Destination "$env:USERPROFILE\.codex\skills\codex-doc-first-development" `
  -Recurse `
  -Force
```

Then start a new Codex thread or refresh available skills and invoke:

```text
Use $codex-doc-first-development to turn my software idea into a Codex-ready engineering plan.
```

## What It Does

- Selects quick, standard, or strict workflow mode.
- Captures product ideas and converts them into `REQ-*` requirements.
- Creates a Codex-friendly docs source of truth.
- Generates phase plans and Task Packs.
- Defines subagent, branch, file ownership, lock, and CI rules.
- Guides TDD, validation, acceptance, docs writeback, PR preparation, and archival.

## Scripts

Scaffold docs:

```powershell
python .\codex-doc-first-development\scripts\scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001
```

Check a Task Pack:

```powershell
python .\codex-doc-first-development\scripts\check_task_pack.py "C:\path\to\project\docs\delivery\tasks\TASK-001.md"
```

## User Guide

See [docs/user-guide.md](docs/user-guide.md).

