# Domain Pain-Point Cards Repository

This document contains 6 core domain pain-point cards. During `CoT Intake Reflection`, agents match user inputs against these cards using rule-based feature counting to proactively diagnose deep engineering risks.

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
  - $0.5 \le S(C) < 0.8$: Mid confidence. Require `user_confirmed: true` in Task Pack.
  - $S(C) < 0.5$: Low/No match. Fall back to standard passive CoT intake.
- **Top-1 Exclusivity**: Only the highest scoring card with $S(C) \ge 0.5$ is activated. Lower scoring candidates are logged in `ignored_candidates`.

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
  "inspection_cmd": "python scripts/check_permission_log.py docs/delivery/permission-audit.log",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Simultaneous state mutation across multiple async workers or threads causing non-deterministic data corruption or deadlock.

### Mandatory Inspection Checklist
1. Verify single-writer mutex or transactional file locking.
2. Confirm state modifications are atomic.
3. Add stress tests for concurrent execution paths.

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
  "inspection_cmd": "Call the Skill tool with \"codex-doc-first-doc-sync\" (runs scripts/check_docs_links.py over docs)",
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
  "inspection_cmd": "python scripts/verify_runtime_trace.py --mode goal --json",
  "version": "1.0.0",
  "last_validated": "2026-07-28"
}
```

### Risk Description
Bypassing authorization middleware, exposing sensitive secrets in version control, or granting excessive scope.

### Mandatory Inspection Checklist
1. Validate access token signature and scope bounds.
2. Ensure secrets are loaded from environment variables, never hardcoded.
3. Verify permission enforcement on every API endpoint.
