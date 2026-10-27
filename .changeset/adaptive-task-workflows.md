---
"codex-doc-first-development-skill": minor
---

Adapt lifecycle artifacts and design gates to task risk. Quick work reuses existing
records or one brief; Standard and Strict maintain applicable contracts and gates.
Reuse established authorization and approved designs, skip visual artifacts for
non-UI work, and distinguish Task Pack structure from execution authority. Preserve
selected runtime protocols, skill invocation policy, script ownership, and CLI
exit codes/JSON interfaces. Add applicability regressions and installed command
checks, and correct residual path examples and a Ruff line-length failure.

Fix an observed fail-open runtime gate: missing required inputs and malformed
JSON records now return existing Exit 3 rather than silently passing. Goal requires
an explicit valid MAX_ITERATIONS. Missing optional expansions remain supported;
malformed existing expansions fail closed. Initialized empty audit/trace states
remain supported. No exit code or payload shape changes.
