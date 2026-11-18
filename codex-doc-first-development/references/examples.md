# Workflow Examples

Use [Adaptive Workflow](adaptive-workflow.md) to select scope, records, and
checks. These examples show what counts as a closed plan point.

## Quick: Correct a README typo

The project has no task record. Confirm the affected file and expected wording
before editing. Review the actual diff. If no links or anchors changed and no
project rule requires another check, report the diff inspection in the final
reply. Do not create a task file, log, audit lock, or phase archive.

## Standard: Add CLI JSON output

Reuse the existing export task. Before editing, record the command contract,
allowed files, and checks for correct JSON, unchanged default output, and
errors. Update the CLI contract in its owning doc. After testing, append the
executed command, result, and any limitations to that same task. Do not start
a second Task Pack, independent verification report, or visual design.

## Strict: Change a permission rule in one file

Record the affected access rule and accepted/denied cases in one existing task.
Update the owning contract and verify allowed and denied access for the
affected roles. Review the actual diff and link the results from the same task.
The size of the diff does not lower the risk tier. If the project has no audit
requirement, do not generate the skill's transaction logs.

## Explicit audit: Goal fixes a bounded issue

The user explicitly selects the skill's Goal runtime protocol. Keep its
approved whitelist, Task Pack with explicit iteration limit, trace, and log
even for a small fix. Run the installed verifier at protocol checkpoints.
If a required input is missing, stop the dependent action and repair or
restore it; do not infer approval from the brief or an empty replacement.
