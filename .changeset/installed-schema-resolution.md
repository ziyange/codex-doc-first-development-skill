---
"codex-doc-first-development-skill": patch
---

Resolve default runtime schemas relative to the installed skill rather than the
downstream working directory. Preserve explicit schema overrides and fail-close
behavior for missing schemas. Correct the S2 scaffold command, clarify S15 paths,
remove stale CLI version text, and test downstream execution and the 150-line
entrypoint limit. No script moves or protocol changes.
