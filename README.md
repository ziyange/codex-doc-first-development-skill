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
    check_docs_links.py
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

- Performs mandatory structured self-reflection (`## CoT Intake Reflection`): identifies missing inputs, codebase conflicts, and technical feasibility bottlenecks before producing specs.
- Automatically initializes project docs (`/init` action) and creates `AGENTS.md` with auto-detected project commands (`--auto-detect`), including Monorepo and composite stack probing (Makefile, Dockerfile, pnpm-workspace, go.work, Cargo workspace, CMakeLists.txt).
- Selects quick, standard, or strict workflow mode based on impact and risk.
- Captures product ideas and converts them into `REQ-*` requirements with clear acceptance criteria.
- Creates a Codex-friendly docs source of truth (`docs/`).
- Generates phase plans and Task Packs with fine-grained `Allowed Files` scope checking (blocking overly broad wildcards like `*` or `**`).
- Defines subagent, branch, file ownership, lock, and CI rules.
- Guides TDD, anti-fake test quality gates, validation, acceptance, docs writeback, PR preparation, and archival.

The skill is procedural guidance plus two local helper scripts. It does not provide a background scheduler, persistent lock service, CI provider, GitHub credentials, or automatic merge authority.

## Scripts

Scaffold docs with auto-detection of project stack commands:

```powershell
python .\codex-doc-first-development\scripts\scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001 --auto-detect
```

Preview strict mode and opt into applicable documents:

```powershell
python .\codex-doc-first-development\scripts\scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001 --include security --include api --dry-run
```


Check a Task Pack:

```powershell
python .\codex-doc-first-development\scripts\check_task_pack.py "C:\path\to\project\docs\delivery\tasks\TASK-001.md" --json
```

Check documentation relative links and heading anchors:

```powershell
python .\codex-doc-first-development\scripts\check_docs_links.py "C:\path\to\project\docs" --json
```

All helper scripts support `--json` output for seamless integration with GitHub Actions or GitLab CI. The scaffolded Task Pack intentionally contains placeholders and should fail `check_task_pack.py` until completed.

## Validate

```powershell
python -m unittest discover -s tests -v
```

## User Guide

See [docs/user-guide.md](docs/user-guide.md).
