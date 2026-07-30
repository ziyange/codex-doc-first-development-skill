# JSON Schemas Authority Source (v2.1.0)

This document contains human-readable references for `codex-doc-first-development` v2.1.0 governance files. Standard standalone machine-readable JSON Schemas are stored in `references/schemas/*.json`. Python validation scripts load from `references/schemas/*.json` first and fall back to this Markdown file.

## Contents

- [ExecutionTraceSchema](#executiontraceschema)
- [AuditLogSchema](#auditlogschema)
- [ExpansionSchema](#expansionschema)
- [PainPointCardSchema](#painpointcardschema)

## ExecutionTraceSchema

```json
// schema-id: ExecutionTraceSchema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExecutionTraceSchema",
  "type": "object",
  "required": [
    "tx_id",
    "iteration_index",
    "timestamp",
    "action_type",
    "normalized_path",
    "intent_hash",
    "result_status",
    "ignored_candidates"
  ],
  "properties": {
    "tx_id": {
      "type": "string"
    },
    "iteration_index": {
      "type": "integer",
      "minimum": 0
    },
    "timestamp": {
      "type": "string"
    },
    "action_type": {
      "type": "string",
      "enum": ["FILE_WRITE", "FILE_DELETE", "COMMAND_EXEC", "MODE_SWITCH"]
    },
    "normalized_path": {
      "type": "string"
    },
    "intent_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "result_status": {
      "type": "string",
      "enum": ["COMPLETED", "EXPANDED_RESUME", "FUSED_TO_PLAN", "CIRCUIT_BROKEN"]
    },
    "ignored_candidates": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "additionalProperties": false
}
```

## AuditLogSchema

```json
// schema-id: AuditLogSchema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AuditLogSchema",
  "type": "object",
  "required": [
    "tx_id",
    "timestamp",
    "action_type",
    "normalized_path",
    "prev_hash",
    "intent_hash",
    "status"
  ],
  "properties": {
    "tx_id": {
      "type": "string"
    },
    "timestamp": {
      "type": "string"
    },
    "action_type": {
      "type": "string",
      "enum": ["FILE_WRITE", "FILE_DELETE", "COMMAND_EXEC", "PERMISSION_GRANT", "MODE_SWITCH"]
    },
    "normalized_path": {
      "type": "string"
    },
    "prev_hash": {
      "type": "string"
    },
    "intent_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "status": {
      "type": "string",
      "enum": ["PENDING", "COMMITTED", "ABORTED"]
    }
  },
  "additionalProperties": false
}
```

## ExpansionSchema

```json
// schema-id: ExpansionSchema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExpansionSchema",
  "type": "object",
  "required": [
    "expansion_seq",
    "tx_id",
    "approved_pattern",
    "approved_at",
    "approved_by"
  ],
  "properties": {
    "expansion_seq": {
      "type": "integer",
      "minimum": 1
    },
    "tx_id": {
      "type": "string"
    },
    "approved_pattern": {
      "type": "string"
    },
    "approved_at": {
      "type": "string"
    },
    "approved_by": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

## PainPointCardSchema

```json
// schema-id: PainPointCardSchema
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PainPointCardSchema",
  "type": "object",
  "required": [
    "card_id",
    "title",
    "category",
    "trigger_rules",
    "inspection_cmd",
    "version",
    "last_validated"
  ],
  "properties": {
    "card_id": {
      "type": "string",
      "pattern": "^[A-Z0-9_]+$"
    },
    "title": {
      "type": "string"
    },
    "category": {
      "type": "string",
      "enum": [
        "CONCURRENCY_RACE",
        "STATE_MEMORY_LEAK",
        "SCHEMA_MIGRATION",
        "CROSS_PLATFORM",
        "PERFORMANCE_DEGRADATION",
        "SECURITY_PERMISSION"
      ]
    },
    "trigger_rules": {
      "type": "object",
      "required": ["mandatory_keywords", "pattern_contexts"],
      "properties": {
        "mandatory_keywords": {
          "type": "array",
          "items": { "type": "string" }
        },
        "pattern_contexts": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "additionalProperties": false
    },
    "inspection_cmd": {
      "type": "string"
    },
    "version": {
      "type": "string"
    },
    "last_validated": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```
