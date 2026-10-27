# AGENTS.md

Instructions for coding agents working **in this repository** (the skills distribution repo itself). For instructions on *using* the skills in a downstream project, install the skill and follow its `SKILL.md`.

> `CLAUDE.md` is a symlink to this file; Claude Code and Codex read the same instructions.

## Repository map

```text
.
├── codex-doc-first-development/      # Main orchestrator skill (installable unit)
│   ├── SKILL.md                      # Entry point: governance rules, S0-S22 workflow, script index
│   ├── agents/openai.yaml            # Codex UI metadata
│   ├── references/                   # 9 methodology docs + schemas/ (5 standalone JSON, the authority)
│   └── scripts/                      # Hard gates: verify_runtime_trace, check_permission_log,
│                                     #   lock_manager, scaffold_docs
├── codex-doc-first-doc-sync/         # Companion skill: doc sync discipline + check_docs_links.py
├── codex-doc-first-task-pack-gate/   # Companion skill: Task Pack gate + check_task_pack.py
├── codex-doc-first-ui-ux-prototyping/# Companion skill: pre-dev UI/UX alignment gate (no scripts)
├── codex-doc-first-start/            # Companion skill: user-invoked human entry point
├── tests/                            # unittest suite (no pytest); fixtures/ drive the CLI end-to-end
├── docs/user-guide.md                # Chinese user manual
├── .agents/invocation.md             # Invocation model (user-invoked vs model-invoked)
├── GLOSSARY.md                       # Shared vocabulary
├── SCOPE.md                          # Contribution bar and non-goals
├── .out-of-scope/                    # Rejected concepts and why
├── .changeset/                       # Versioning changesets
└── CHANGELOG.md                      # Keep a Changelog history
```

The repo root (README, tests, CI, docs) is the development shell. Each `codex-doc-first-*/` directory is a self-contained installable skill copied as a whole to the agent's skills directory.

## Commands

```bash
# Full test suite (unittest is the only runner; pytest config was removed)
python -m unittest discover -s tests -v

# Docs self-check (dogfooding: the repo's own gates must stay green)
python codex-doc-first-doc-sync/scripts/check_docs_links.py . --json
python codex-doc-first-task-pack-gate/scripts/check_task_pack.py tests/fixtures/valid_task_pack.md --json

# End-to-end hard gate on fixtures
python codex-doc-first-development/scripts/verify_runtime_trace.py \
  --trace tests/fixtures/valid_trace.json \
  --permission-log tests/fixtures/valid_audit.log \
  --task-pack tests/fixtures/valid_task_pack.md \
  --schemas codex-doc-first-development/references/schemas.md \
  --mode goal --next-iteration 1 --json
```

Requires Python >= 3.9 and `jsonschema` (see `requirements.txt`).

## Bilingual policy

- Skill internals (`SKILL.md`, `references/`, scripts, repo-level convention files): **English**.
- `README.md` and `docs/user-guide.md`: **Chinese** (project convention for the primary audience).
- Local design drafts (`AI 文档优先软件开发方法论.md`, `Codex 文档优先软件开发方法论.md`) are gitignored; the installable skill is the runtime source of truth.

## Skill authoring conventions

1. **Register the invocation axis.** Every skill is user-invoked or model-invoked per `.agents/invocation.md`; set frontmatter and `agents/openai.yaml` accordingly and keep both harnesses in sync.
2. **Keep `SKILL.md` lean** (<= 150 lines). It is the progressive-disclosure entry point; details live in the skill's own `references/` or sibling files.
3. **`short_description`**: 25-64 characters, verb phrase, no trailing period.
4. **References with a Contents section**: any reference doc longer than ~100 lines gets a Contents list with GFM-correct anchors (underscores kept, `&` dropped without collapsing spaces). `tests/test_doc_sync.py` enforces the slug rules; CI runs the link checker on the repo.
5. **Scripts belong to exactly one skill.** Shared gates live in the orchestrator; a discipline-specific checker moves with its companion skill. Never keep two copies of a script.
6. **Schema authority**: `references/schemas/*.json` in the owning skill is the machine-readable source of truth; `references/schemas.md` is the degradation fallback and must deep-match the JSON (enforced by `tests/test_schemas_parity.py`).
7. **Tests are mandatory** for behavior changes. New gates need fixture-driven cases; doc claims need parity/anchor tests. The suite must stay green on all three OSes in CI.
8. **Cross-skill references** use `Call the Skill tool with "<name>"`, never deep relative links and never bare `/name` mentions in operative instructions.

## Versioning

Version bumps go through changesets: add a `.changeset/<name>.md` file with the bump type (`major`/`minor`/`patch`) and a summary, and let the release workflow open the version PR. The skill version lives in `pyproject.toml` and the `SKILL.md` title; keep them in sync. Breaking changes (e.g. moving a script between skills) are called out explicitly in the changeset.

Preview the non-npm release plan with `python .github/scripts/release_version.py --json`.
The repository-level release helper belongs to the development shell, not an installable skill.
See [docs/releasing.md](docs/releasing.md) for version PR validation and tag publication.

## Contributing

Read [SCOPE.md](./SCOPE.md) first: every change needs an observed failure and a fit with the philosophy (docs as single source of truth, fail-close, evidence over assertion). Rejected ideas are archived in `.out-of-scope/`.
