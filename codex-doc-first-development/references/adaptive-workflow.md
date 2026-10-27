# Adaptive Workflow

Read this before selecting stages or artifacts. This is the applicability policy
for the lifecycle, review gates, templates, and prompts; those resources describe
the applicable stage's mechanics. Higher-priority instructions and explicit user
choices remain authoritative.

## Choose a Risk Tier

Inspect the repository, existing docs, change scope, and known authorization first.
Choose the highest applicable tier by impact, not file count:

| Tier | Trigger | Required record | Applicable stages and checks |
|---|---|---|---|
| Quick | Clear, bounded, low-risk task without architecture or public-contract changes | Reuse an existing task or doc; otherwise one brief task record | Intake/scope, implementation, relevant verification, acceptance/writeback |
| Standard | Nontrivial features, behavior changes, or cross-module work that exceed Quick's bounded low-risk scope and have no Strict trigger | Affected requirements/contracts, Task Pack, verification evidence; phase plan only for multiple tasks | Relevant S0-S22 stages; Task Pack and relevant tests |
| Strict | Security, permissions, migrations, public contracts, major architecture, or material production risk | Full applicable source-of-truth docs, Task Packs, phase plan, runtime audit | Full applicable lifecycle, runtime gate, meaningful tests and risk review |

Quick record: goal, allowed files, acceptance criteria, and verification command
and result. Before implementation, specify the command and expected outcome;
afterward, record the actual result. An existing record that already covers these
facts is sufficient. Do not initialize a docs tree just to satisfy a small task.
Record a documentation-only task's relevant check; do not invent code tests.

Standard and Strict reuse existing documents. Create only missing applicable
artifacts, preserving the repository's established paths and conventions. The
scaffolder is an explicit initialization helper, not a required intake action;
its existing `--mode quick` output remains available for users who request it.

## Keep Autonomy Separate

Quick/Standard/Strict describe risk and artifacts. Goal/Plan/Build describe
execution authorization and iteration behavior. Keep the user's chosen autonomy
mode; do not silently switch it or choose Build to avoid audit requirements.
If none is selected, use the host's existing authorization model without inventing
a separate mode-selection handshake. Configure an explicit mode when runtime audit
is required; ask if the choice changes authorization or cannot be inferred.

Explicit Goal, Plan, Build runtime protocols or user-required auditing retain their
Task Pack, audit, whitelist/blacklist, iteration, and mode-switch requirements even
for Quick work. A brief is not a substitute for a runtime gate's inputs. Strict
requires runtime audit. Missing or invalid required inputs remain blocking.
Initialize trace/log files explicitly before the first action; an initialized
empty audit log and an empty trace array represent a clean state, not a missing
file. Goal requires one explicit `MAX_ITERATIONS: N` line with N in 1..10.

## Apply Design Gates to Changed Surfaces

- No graphical UI change: skip visual prototypes, image generation, and graphical
  binding tables. Verify CLI arguments/output, backend contracts, or script behavior.
- Graphical UI change: reuse confirmed designs and review changed screens, states,
  and interactions before coding. Generate new mockups when visual decisions need
  alignment; do not regenerate approved screens for unrelated changes.
- UI with an API: record the affected API bindings and feedback states.
- Local-only UI: record events, local state, and outcomes; no invented API layer.
- Shared external requests: reuse appropriate service/client modules. Use field
  projection only when consumer or performance requirements justify it; preserve
  existing contracts and avoid adding generic endpoints to satisfy a template.

## Keep Interaction Focused

Open with a short statement of the task, selected tier and reason, scope, and
verification approach. Explain material uncertainties and decisions, not private
reasoning or a prescribed reflection transcript. Inspect discoverable facts first;
ask only questions whose answers change the result or establish missing authority.
Reuse existing authorization; no repeated approval for the same action and scope.
New external actions and scope expansion still need the applicable authorization.

If new evidence raises risk, explain why, update affected docs and gate inputs,
and pause only work dependent on unresolved scope, authority, or design decisions.
Already authorized high-risk work still gets Strict checks without asking the user
to authorize the same action again.

## Interpret Evidence Correctly

A Task Pack checker pass proves structural checks passed. It does not grant user
authorization, resolve dependencies, execute tests, or replace runtime validation.
Warnings are advisory; review their effect on acceptance without treating them as
either structural failure or test success. Review scripts using their owning skill
paths and project artifacts using project paths.

When blocked, report the failed check, affected work, and smallest recovery action.
Never fabricate successful checks. Retain existing exit codes and JSON payloads.
Update affected docs before or alongside changed facts; a behavior-preserving
internal refactor needs no doc edit when documented facts remain unchanged.
