# Domain Pain-Point Cards Repository

Use these cards only for relevant domain risks. Consult [Adaptive Workflow](adaptive-workflow.md) for verification and audit applicability. The command fields are examples: prefer a targeted project check that tests the changed behavior. The unittest examples apply only to Python projects with that runner; the links example applies only to Markdown path issues.
Run applicable commands from the project root. Replace `<skill-root>` and `<project-root>` with actual paths and quote paths containing spaces.

## Contents

- [Matching & Confidence Rules](#matching--confidence-rules)
- [Card 1: CONCURRENCY_RACE](#card-1-concurrency_race)
- [Card 2: STATE_MEMORY_LEAK](#card-2-state_memory_leak)
- [Card 3: SCHEMA_MIGRATION](#card-3-schema_migration)
- [Card 4: CROSS_PLATFORM](#card-4-cross_platform)
- [Card 5: PERFORMANCE_DEGRADATION](#card-5-performance_degradation)
- [Card 6: SECURITY_PERMISSION](#card-6-security_permission)

## Matching & Confidence Rules

- **Binary Feature Hits**: Mandatory keywords and pattern context rules count as binary (0 or 1) hits.
- **Weighted Formula**:
  $$S(C) = \frac{2.0 \times N_{\text{mandatory-hits}} + 1.0 \times N_{\text{pattern-hits}}}{2.0 \times N_{\text{mandatory-total}} + 1.0 \times N_{\text{pattern-total}}}$$
- **Thresholds**:
  - $S(C) \ge 0.8$: High confidence match. Trigger targeted inspection checklist.
  - $0.5 \le S(C) < 0.8$: Tentative match. Check repository evidence and ask only if a material decision is still missing.
  - $S(C) < 0.5$: Low/No match. Continue ordinary repository intake without a domain checklist.
- **Top-1 selection**: Start with the strongest match. Inspect other applicable risks if they affect acceptance. Record only material findings in the closure record. Preserve machine fields required by projects already using structured cards.

---

## Card 1: CONCURRENCY_RACE

```json
{
  "card_id": "CONCURRENCY_RACE",
  "title": "Concurrency & Asynchronous Race Condition Risk",
  "category": "CONCURRENCY_RACE",
  "trigger_rules": {
    "mandatory_keywords": ["concurrent", "async", "lock", "mutex", "thread", "parallel", "race"],
    "pattern_contexts": ["shared_state", "shared_resource", "atomic", "queue", "worker"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Simultaneous state mutation across multiple async workers or threads causing non-deterministic data corruption or deadlock.

### Mandatory Inspection Checklist
1. Verify the affected shared state boundaries and coordination mechanism.
2. Check concurrent updates and relevant failure or recovery cases.
3. Inspect the audit lock only if the change affects an active audit protocol.

---

## Card 2: STATE_MEMORY_LEAK

```json
{
  "card_id": "STATE_MEMORY_LEAK",
  "title": "State Accumulation and Memory Leak Risk",
  "category": "STATE_MEMORY_LEAK",
  "trigger_rules": {
    "mandatory_keywords": ["memory", "leak", "listener", "subscriber", "cache", "retain"],
    "pattern_contexts": ["global_state", "event_emitter", "unsubcribe", "cleanup", "lifecycle"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Unbounded cache growth, unremoved event listeners, or persistent global state retention across long-running component lifecycles.

### Mandatory Inspection Checklist
1. Inspect event listener removal and cleanup hooks.
2. Verify cache TTL or LRU eviction bounds.
3. Validate memory usage under sustained load.

---

## Card 3: SCHEMA_MIGRATION

```json
{
  "card_id": "SCHEMA_MIGRATION",
  "title": "Breaking Data or Interface Schema Migration",
  "category": "SCHEMA_MIGRATION",
  "trigger_rules": {
    "mandatory_keywords": ["migration", "schema", "database", "field_delete", "rename", "breaking"],
    "pattern_contexts": ["column_remove", "type_change", "backwards_compatibility", "sql", "orm"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Deleting or renaming database columns or public API fields that break existing callers or persisted storage formats.

### Mandatory Inspection Checklist
1. Confirm two-phase migration (add new field -> backfill -> deprecate old field).
2. Validate backwards compatibility with legacy payloads.
3. Verify database rollback scripts.

---

## Card 4: CROSS_PLATFORM

```json
{
  "card_id": "CROSS_PLATFORM",
  "title": "Cross-Environment & OS Path Inconsistency",
  "category": "CROSS_PLATFORM",
  "trigger_rules": {
    "mandatory_keywords": ["windows", "linux", "mac", "path", "os", "cross_platform", "case_sensitivity"],
    "pattern_contexts": ["backslash", "slash", "symlink", "file_system", "encoding"]
  },
  "inspection_cmd": "python <skill-root>/scripts/check_docs_links.py <project-root>/docs --json",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Path handling failures due to hardcoded backslashes, OS-specific newline conventions, or file system case insensitivity.

### Mandatory Inspection Checklist
1. Enforce forward-slash path normalization (`normalized_path`).
2. Test on both Windows (pwsh) and POSIX environments.
3. Verify case-fold matching for glob whitelist evaluations.

---

## Card 5: PERFORMANCE_DEGRADATION

```json
{
  "card_id": "PERFORMANCE_DEGRADATION",
  "title": "N+1 Query & Unbounded Loop Performance Bottleneck",
  "category": "PERFORMANCE_DEGRADATION",
  "trigger_rules": {
    "mandatory_keywords": ["performance", "slow", "n+1", "latency", "benchmark", "query"],
    "pattern_contexts": ["loop_query", "fetch_in_loop", "unindexed", "batch", "pagination"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Executing database queries or external HTTP requests inside loops without batching or pagination limits.

### Mandatory Inspection Checklist
1. Replace in-loop queries with bulk batch operations.
2. Verify index presence for queried fields.
3. Enforce maximum limit/pagination parameters.

---

## Card 6: SECURITY_PERMISSION

```json
{
  "card_id": "SECURITY_PERMISSION",
  "title": "Privilege Escalation & Unauthorized Resource Access",
  "category": "SECURITY_PERMISSION",
  "trigger_rules": {
    "mandatory_keywords": ["security", "permission", "auth", "rbac", "token", "escalation", "secret"],
    "pattern_contexts": ["jwt", "bearer", "authorization", "unauthorized", "bypass", "credential"]
  },
  "inspection_cmd": "python -m unittest discover -s tests",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Bypassing authorization middleware, exposing sensitive secrets in version control, or granting excessive scope.

### Mandatory Inspection Checklist
1. Test allowed and denied actions for affected roles and entry points.
2. Check token, scope, and secret handling when changed.
3. Do not select the bundled runtime audit based on a card match; a trace of agent actions cannot verify the product's permission behavior.
