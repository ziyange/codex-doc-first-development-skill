# Codex Doc-First Development Skill

Practical document-first software development workflow for Codex.

This repository contains a reusable Codex skill that guides raw software ideas or existing repository changes through requirements, an approved docs source of truth, phase plans, Task Packs, authorized subagent delegation, validation gates, PR/merge preparation, and archive records.

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

## Install With Codex

Recommended: send this GitHub skill URL to Codex and ask it to install the skill.

```text
Use $skill-installer to install this Codex skill:
https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

Codex should install it into your `$CODEX_HOME/skills` directory, or `~/.codex/skills` when `CODEX_HOME` is unset. Restart or refresh Codex only if the new skill is not discovered immediately.

The equivalent command belongs to the installed `skill-installer` skill; it is not a script in this repository:

```bash
scripts/install-skill-from-github.py --url https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

Manual fallback:

```powershell
Copy-Item `
  -LiteralPath ".\codex-doc-first-development" `
  -Destination "$env:USERPROFILE\.codex\skills\codex-doc-first-development" `
  -Recurse `
  -Force
```

## Use

```text
Use $codex-doc-first-development to turn my software idea into a Codex-ready engineering plan.
```

Chinese prompt:

```text
使用 $codex-doc-first-development，从这个项目想法开始，帮我生成需求、docs 事实源、阶段计划、Task Pack、验证门禁和归档流程：
<<<粘贴项目想法>>>
```

## What It Does

- Selects quick, standard, or strict workflow mode.
- Captures product ideas and converts them into `REQ-*` requirements.
- Creates a Codex-friendly docs source of truth.
- Generates phase plans and Task Packs.
- Defines subagent, branch, file ownership, lock, and CI rules.
- Guides TDD, validation, acceptance, docs writeback, PR preparation, and archival.

The skill is procedural guidance plus two local helper scripts. It does not provide a background scheduler, persistent lock service, CI provider, GitHub credentials, or automatic merge authority.

## Scripts

Scaffold docs:

```powershell
python .\codex-doc-first-development\scripts\scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001
```

Preview strict mode and opt into applicable documents:

```powershell
python .\codex-doc-first-development\scripts\scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001 --include security --include api --dry-run
```

Check a Task Pack:

```powershell
python .\codex-doc-first-development\scripts\check_task_pack.py "C:\path\to\project\docs\delivery\tasks\TASK-001.md"
```

The scaffolded Task Pack intentionally contains placeholders and should fail this check until it is completed.

## Validate

```powershell
python -m unittest discover -s tests -v
```

## User Guide

See [docs/user-guide.md](docs/user-guide.md).
