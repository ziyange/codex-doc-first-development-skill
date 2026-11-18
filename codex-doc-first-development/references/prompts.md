# Prompt Pack

These optional prompts start specific parts of the work. Use
[Adaptive Workflow](adaptive-workflow.md) to select records and checks.

## Start From Zero

```text
Use $codex-doc-first-development for this project:
<<<idea and constraints>>>

Inspect the context, identify the first independently verifiable outcome, and
propose its scope, acceptance criteria, and verification. Ask only about material
unknowns. Initialize docs only if needed; use the owning docs for changed facts.
```

## Existing Repository Intake

```text
Use $codex-doc-first-development for this change:
<<<goal and scope>>>

Inspect affected files, docs, tests, and project rules. Reuse the existing task
record if possible. Tell me how you will verify the outcome before editing.
```

## Formal Solution

```text
For the changed design, define scope, observable behavior, affected contracts,
dependencies, failure paths, and checks. Resolve risks that affect implementation;
keep agreed facts in their owning documents.
```

## Pre-Dev UI/UX and Prototype Alignment

```text
Review the changed graphical screens, states, and interactions before dependent
implementation. Reuse approved designs. For local-only UI, map events to local
state and outcomes. For API-backed UI, document affected bindings.
```

## Phase and Worker Work

```text
Order independently verifiable outcomes by dependency and record each once.
If I have authorized workers, assign disjoint scopes and define which evidence
they should return. Preserve approved contracts and existing user changes.
```

## Acceptance Review

```text
Compare the actual diff and check results with scope, owning docs, and acceptance.
Inspect relevant failure paths, distinguish local and CI evidence, and record
the actual outcome or blocker in the existing task. Keep verification links
rather than copying reports into separate files.
```
