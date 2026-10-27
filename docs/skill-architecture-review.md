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

## Second Review: Adaptive Workflow

Baseline: 2836d48. User-approved priorities: proportional task routing and reuse
of existing docs or one brief for bounded low-risk work. No script moves, new
public JSON fields, or exit-code changes are introduced.

| Dimension | Previous / 20 | Revised / 20 | Evidence |
|---|---:|---:|---|
| Discovery and invocation | 17 | 19 | Shorter capability description, risk-based picker prompts, unchanged invocation policy |
| Progressive disclosure | 17 | 18 | One applicability policy; main entrypoint remains below 150 lines |
| Installation portability | 19 | 19 | Companion examples use owning skill paths; downstream command checks |
| Executable verification | 19 | 20 | Missing/corrupt runtime inputs now fail closed; explicit Goal limits validated |
| Maintenance consistency | 18 | 18 | Cross-reference and rule drift guards; existing release automation limitation remains |
| Total | 90 / 100 | 94 / 100 | Reviewer judgment, not a measured task-success rate |

An independent baseline pass reproduced conflicting instructions for Quick,
non-UI tasks, repeated authorization, and structural Task Pack readiness. The
forward review applied the revised skills to ten scenarios; it found two remaining
routing ambiguities and an inherited runtime fail-open defect. The author fixed
these findings and ran the full suite; this is not a second independent review.

| Scenario | Final intended outcome |
|---|---|
| Authorized README typo | Quick; reuse existing task/doc and relevant documentation check |
| Small authorized bug without docs | Quick brief; targeted meaningful regression verification |
| Pure CLI feature | Standard CLI contracts/Task Pack; no visual prototype |
| Backend public API change | Strict contracts and runtime audit; no graphical UX gate |
| Approved GUI label adjustment | Quick; reuse existing approval/mockup, update changed fact |
| Local-only graphical UI | Standard events/state/outcomes; no invented API |
| Single-file permission migration | Strict by impact, permission/migration tests and audit |
| Already authorized commit/push | Reuse scope-specific authorization; verify destination/checks |
| Structurally passed Task Pack, no authority | No implementation; resolve missing authorization |
| Explicit Goal, small task | Quick risk plus complete Goal protocol inputs and valid iteration limit |

Rulings and evidence:

- Work stayed in the supplied checkout on a dedicated branch rather than creating
  a second worktree. The checkout was clean; this preserves the user's workspace
  location, but branch isolation does not provide a separate filesystem.
- The runtime repair is included because independent execution returned SUCCESS
  for missing required inputs, contradicting the preserved fail-close guarantee.
  Tests failed before the fix. Missing/corrupt records now return existing Exit 3;
  initialized empty logs/traces and absent optional expansions remain supported.
- Explicit Quick scaffolder output stays compatible. The agent avoids invoking
  it unnecessarily; the helper is still available on request.
- Automated documentation tests check routing discoverability and known conflicting
  instructions, not agent understanding. The independent scenario review supplies
  behavioral evidence; no latency, token-cost, or user-satisfaction gain is claimed.
- Local Ruff and the full unittest suite pass. Repository links, valid Task Pack,
  and fixture runtime checks pass. Remote three-platform CI is checked after push.
- The first remote matrix failed before tests: setup-python could not install
  Python 3.9 on the new Ubuntu 26.04 `latest` image. The official Python manifest
  provides 3.9 on Ubuntu 24.04 and macOS x64. The test matrix now pins Ubuntu
  24.04, Windows 2022, and macOS 15 Intel, retaining Python 3.9/3.12 and disabling
  fail-fast so each platform reports its own evidence.
- The baseline Release workflow failed because changesets/action expected a
  package.json in a deliberately non-npm repository. Repairing release automation
  is deferred; the pending patch and minor changesets are retained. No release
  version bump or successful automatic release is claimed.

## Release Repair Follow-Up

The previously deferred npm-only release failure is addressed by the repository's
Python changeset planner and Version Skills PR workflow; see [Release Maintenance](releasing.md).
Historical red runs remain attached to their original commits. Current CI and the
generated version branch must be assessed separately by commit SHA. The user
explicitly authorized enabling the combined Actions create/approve-PR repository
setting; workflows create version PRs only, and default permissions stay read-only.
