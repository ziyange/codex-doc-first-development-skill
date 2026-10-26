# Skill Architecture Review

Review date: 2026-10-27. Baseline: 9217c63, version 2.3.0.

## Assessment and Plan

Scores are reviewer judgments, not empirical agent-success percentages. Each
dimension has equal weight. The review covers the five installable directories,
their invocation metadata, reference routing, executable gates, and tests.

| Dimension | Before / 20 | After / 20 | Evidence |
|---|---:|---:|---|
| Discovery and invocation | 17 | 17 | Five distinct skills; invocation policy parity tests pass |
| Progressive disclosure | 17 | 17 | Main entrypoint is exactly 150 lines; focused references |
| Installation portability | 12 | 19 | Downstream CLI schema failure reproduced and repaired |
| Executable verification | 18 | 19 | Existing 76 tests plus downstream and documented-command regressions |
| Maintenance consistency | 17 | 18 | Actual 150-line ceiling enforced; stale CLI version removed |
| Total | 81 / 100 | 90 / 100 | Architecture is sound; installed execution needed repair |

The narrow plan is to repair installed-path resolution, correct executable
examples, enforce the existing entrypoint budget, and retain current protocols.
Broader restructuring would add risk without an observed failure to justify it.

## Observed Failures and Repairs

1. From a temporary downstream working directory, the runtime verifier returned
   Exit 3 with valid trace, audit, and Task Pack fixtures because the schema
   default was relative to the project. Both library and CLI defaults now resolve
   to the owning skill's bundled schemas. Explicit overrides remain authoritative;
   an explicit missing schema still returns Exit 3.
2. The S2 example omitted mandatory `--root`, producing argparse Exit 2. It now
   includes skill and project roots and previews changes with `--dry-run`.
   A test executes the documented command in a temporary project.
3. The metadata test accepted fewer than 500 lines despite the repository's
   150-line ceiling. It now enforces at most 150. The existing entrypoint already
   met that limit; no size violation or unnecessary rewrite is claimed.
4. CLI help advertised v2.2.0 while the distribution was v2.3.0. The help text now
   describes its purpose without duplicating release metadata.

## Remaining Limitations

- Instructions still use the abstract Skill tool convention required by the
  repository; a host must map that convention to its own skill-loading mechanism.
- Strong generic architecture prescriptions (field projection and centralized
  request layers) may need applicability judgments in projects without APIs.
  This review did not establish a behavioral failure justifying changes to them.
- Local validation covers Windows. Linux and macOS confidence depends on CI;
  this review does not claim those jobs have executed.
- Merkle consistency is a gate on supplied records, not proof that every external
  action was captured. Behavioral adherence still needs realistic session review.

## Validation and Release

Run the full unittest suite, repository link checker, valid Task Pack checker,
and fixture runtime gate before publishing. An independent read-only agent pass
reproduced the two downstream command failures. The changeset requests a patch;
release automation owns version bumps, so 2.3.0 metadata remains synchronized.
Install all five directories together and compare their file hashes to the
verified Git commit; keep a backup of the previous local installation.
