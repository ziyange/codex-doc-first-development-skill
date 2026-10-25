#!/usr/bin/env python3
"""
verify_runtime_trace.py - Runtime Trace & Audit Log Hard Gate CLI

Verifies execution-trace.json and permission-audit.log against v2.2.0 governance specifications.
Returns Exit Codes 0 to 6 with structured --json outputs.
"""

import os
import sys
import json
import argparse
import fnmatch
import re
from typing import List, Dict, Tuple, Optional

# Import internal check_permission_log helper module
try:
    from check_permission_log import (
        normalize_path,
        verify_merkle_chain,
        parse_audit_log,
    )
except ImportError:
    # Handle relative import when running from package directory
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from check_permission_log import (
        normalize_path,
        verify_merkle_chain,
        parse_audit_log,
    )

# Try importing jsonschema for schema validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


BUILD_MODE_BLACKLIST = [
    ".git/*",
    "**/*.pem",
    "**/*.key",
    "**/.env*",
    "docs/delivery/.log.lock",
    "docs/delivery/permission-audit.log",
    "docs/delivery/execution-trace.json",
    "docs/delivery/expansions.json",
]


def load_schema_from_markdown(schemas_md_path: str, schema_id: str) -> Optional[Dict]:
    """
    Loads JSON Schema. Prioritizes standalone JSON file under references/schemas/<schema_id>.json.
    Falls back to parsing references/schemas.md anchor `// schema-id: <id>` for backward compatibility.
    Fail-close: returns None if missing or invalid.
    """
    # 1. Try loading standalone JSON file
    if schemas_md_path:
        schemas_dir = os.path.join(os.path.dirname(schemas_md_path), "schemas")
        standalone_json_path = os.path.join(schemas_dir, f"{schema_id}.json")
        if os.path.exists(standalone_json_path):
            try:
                with open(standalone_json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    # 2. Fallback to extracting from Markdown file
    if not os.path.exists(schemas_md_path):
        return None

    try:
        with open(schemas_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        target = f"// schema-id: {schema_id}"
        if target not in content:
            return None

        # Extract json block following anchor
        start_idx = content.find(target)
        json_start = content.find("{", start_idx)
        if json_start == -1:
            return None

        # Simple brace counting parser for valid JSON block
        brace_count = 0
        json_end = -1
        for i in range(json_start, len(content)):
            if content[i] == "{":
                brace_count += 1
            elif content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break

        if json_end == -1:
            return None

        json_str = content[json_start:json_end]
        return json.loads(json_str)
    except Exception:
        return None


def validate_schema(data: Dict, schema: Dict) -> bool:
    """Validates data against JSON schema if jsonschema is installed."""
    if not HAS_JSONSCHEMA:
        # Fallback basic requirement check if jsonschema package missing
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                return False
        return True

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.ValidationError:
        return False


def parse_trace_file(file_path: str) -> List[Dict]:
    """Parses execution-trace.json."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            if content.startswith("["):
                return json.loads(content)
            else:
                return [json.loads(line) for line in content.splitlines() if line.strip()]
    except Exception:
        return []


def parse_task_pack(file_path: str) -> Tuple[List[str], int]:
    """
    Parses TASK-xxx.md for Allowed Files and MAX_ITERATIONS.
    """
    allowed_files = []
    max_iterations = 5  # Default limit

    if not os.path.exists(file_path):
        return allowed_files, max_iterations

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        in_allowed = False
        for line in lines:
            line_str = line.strip()
            if "MAX_ITERATIONS:" in line_str or "max_iterations:" in line_str:
                parts = line_str.split(":")
                if len(parts) > 1:
                    try:
                        max_iterations = int(parts[1].strip())
                    except ValueError:
                        pass
            elif "Allowed Files" in line_str or "allowed_files" in line_str:
                in_allowed = True
                continue
            elif in_allowed:
                if line_str.startswith("#") or line_str.startswith("##"):
                    in_allowed = False
                elif line_str.startswith("-") or line_str.startswith("*"):
                    item = line_str.lstrip("-* ").strip("` ")
                    # Skip empty items and sentence-style non-patterns
                    # (e.g. "None outside Allowed Files." must not become a glob)
                    if item and not re.match(r"(?i)^(?:none|n/a)\b", item):
                        allowed_files.append(item)
    except Exception:
        pass

    return allowed_files, max_iterations


def parse_expansions_file(file_path: str) -> List[Dict]:
    """Parses docs/delivery/expansions.json."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content) if content.startswith("[") else []
    except Exception:
        return []


def matches_glob(path_str: str, patterns: List[str]) -> bool:
    """Checks if a normalized path matches any glob in patterns."""
    norm = normalize_path(path_str)
    for pat in patterns:
        norm_pat = normalize_path(pat)
        if fnmatch.fnmatch(norm, norm_pat):
            return True
    return False


def run_verification(
    trace_path: str,
    log_path: str,
    task_pack_path: str,
    mode: str,
    next_iteration: int,
    schemas_md_path: str = "references/schemas.md",
    expansions_path: str = "docs/delivery/expansions.json",
    runtime_event_reason: Optional[str] = None
) -> Tuple[int, Dict]:
    """
    Executes core verification and returns (exit_code, payload_dict).
    """
    payload = {
        "exit_code": 0,
        "reason": "SUCCESS",
        "runtime_event_reason": runtime_event_reason,
        "scan_truncated": False,
        "mode": mode,
        "next_iteration": next_iteration,
        "expansion_count": 0,
        "max_expansions": 2,
        "offending_files": [],
        "uncommitted_tx_ids": [],
        "reason_details": {},
        "ignored_candidates": []
    }

    # Step 1: Validate schemas presence (Fail-Close Exit 3)
    trace_schema = load_schema_from_markdown(schemas_md_path, "ExecutionTraceSchema")
    audit_schema = load_schema_from_markdown(schemas_md_path, "AuditLogSchema")
    if not trace_schema or not audit_schema:
        payload["exit_code"] = 3
        payload["reason"] = "SCHEMA_OR_PARSE_FAILURE"
        return 3, payload

    # Parse inputs
    trace_entries = parse_trace_file(trace_path)
    audit_entries = parse_audit_log(log_path)
    allowed_files, max_iterations = parse_task_pack(task_pack_path)
    expansions = parse_expansions_file(expansions_path)
    payload["expansion_count"] = len(expansions)

    # Validate Schema structures
    for t_entry in trace_entries:
        if not validate_schema(t_entry, trace_schema):
            payload["exit_code"] = 3
            payload["reason"] = "SCHEMA_OR_PARSE_FAILURE"
            return 3, payload

    for a_entry in audit_entries:
        if not validate_schema(a_entry, audit_schema):
            payload["exit_code"] = 3
            payload["reason"] = "SCHEMA_OR_PARSE_FAILURE"
            return 3, payload

    # Step 2: Goal mode iteration check (Exit 1)
    if mode.lower() == "goal":
        if next_iteration > max_iterations:
            payload["exit_code"] = 1
            payload["reason"] = "ITERATION_EXCEEDED"
            return 1, payload

    # Step 3: Merkle Chain verification on audit_entries (Short-circuit Exit 5)
    is_chain_valid, chain_err, failing_idx = verify_merkle_chain(audit_entries)
    if not is_chain_valid:
        payload["exit_code"] = 5
        payload["reason"] = "TAMPER_OR_HASH_MISMATCH"
        payload["scan_truncated"] = True
        return 5, payload

    # Verify expansions.json against Merkle chain PERMISSION_GRANT entries
    grant_tx_ids = {
        e["tx_id"] for e in audit_entries
        if e.get("action_type") == "PERMISSION_GRANT" and e.get("status") == "COMMITTED"
    }
    for exp in expansions:
        if exp.get("tx_id") not in grant_tx_ids:
            payload["exit_code"] = 5
            payload["reason"] = "TAMPER_OR_HASH_MISMATCH"
            payload["scan_truncated"] = True
            return 5, payload

    if len(expansions) > 2:
        payload["exit_code"] = 2
        payload["reason"] = "OFF_BOUNDARY_VIOLATION"
        payload["runtime_event_reason"] = "EXPANSION_LIMIT_EXCEEDED"
        return 2, payload

    # Step 4: Scan AuditLog entries and cross-check with Trace (Short-circuit Exit 6, Exit 4)
    trace_map = {t["tx_id"]: t for t in trace_entries if "tx_id" in t}
    audit_map = {a["tx_id"]: a for a in audit_entries if "tx_id" in a}

    # Find latest MODE_SWITCH index for Post-MODE_SWITCH isolation
    last_mode_switch_idx = -1
    for idx, entry in enumerate(audit_entries):
        if entry.get("action_type") == "MODE_SWITCH":
            last_mode_switch_idx = idx

    # Build Post-MODE_SWITCH approved whitelist for Plan/Goal mode
    approved_patterns = set(allowed_files)
    for idx, entry in enumerate(audit_entries):
        if (
            idx > last_mode_switch_idx
            and entry.get("action_type") == "PERMISSION_GRANT"
            and entry.get("status") == "COMMITTED"
        ):
            approved_patterns.add(entry.get("normalized_path", ""))

    scanned_exit_codes = []

    for a_entry in audit_entries:
        tx_id = a_entry.get("tx_id")
        action_type = a_entry.get("action_type")
        status = a_entry.get("status")
        path = a_entry.get("normalized_path")
        intent_hash = a_entry.get("intent_hash")

        # 3x2 Matrix Check
        t_entry = trace_map.get(tx_id)
        has_result = t_entry is not None

        if status == "PENDING" and has_result:
            payload["exit_code"] = 6
            payload["reason"] = "ILLEGAL_TRANSACTION_STATE"
            payload["reason_details"][tx_id] = "ILLEGAL_PENDING_WITH_RESULT"
            payload["scan_truncated"] = True
            return 6, payload
        elif status == "ABORTED" and has_result:
            payload["exit_code"] = 6
            payload["reason"] = "ILLEGAL_TRANSACTION_STATE"
            payload["reason_details"][tx_id] = "ILLEGAL_ABORTED_WITH_RESULT"
            payload["scan_truncated"] = True
            return 6, payload
        elif status == "PENDING" and not has_result:
            scanned_exit_codes.append(4)
            payload["uncommitted_tx_ids"].append(tx_id)
            payload["reason_details"][tx_id] = "UNCOMMITTED_PENDING"
        elif status == "COMMITTED" and not has_result:
            if action_type != "PERMISSION_GRANT":  # PERMISSION_GRANT is admin-only, doesn't require Result trace
                scanned_exit_codes.append(4)
                payload["uncommitted_tx_ids"].append(tx_id)
                payload["reason_details"][tx_id] = "COMMITTED_RESULT_MISSING"

        # Cross-verify Result intent_hash match
        if t_entry:
            if t_entry.get("intent_hash") != intent_hash:
                payload["exit_code"] = 5
                payload["reason"] = "TAMPER_OR_HASH_MISMATCH"
                payload["scan_truncated"] = True
                return 5, payload

        # Whitelist Boundary Check on writes/deletes
        if action_type in ["FILE_WRITE", "FILE_DELETE"]:
            if mode.lower() == "build":
                if matches_glob(path, BUILD_MODE_BLACKLIST):
                    payload["exit_code"] = 2
                    payload["reason"] = "OFF_BOUNDARY_VIOLATION"
                    payload["offending_files"].append(path)
                    scanned_exit_codes.append(2)
            else:
                # Fail-close: an empty whitelist (no Allowed Files section and no
                # post-MODE_SWITCH PERMISSION_GRANT) never authorizes a write.
                if not matches_glob(path, list(approved_patterns)):
                    payload["exit_code"] = 2
                    payload["reason"] = "OFF_BOUNDARY_VIOLATION"
                    payload["offending_files"].append(path)
                    scanned_exit_codes.append(2)

    # Fail-close: Result traces without a corresponding AuditLog intent entry.
    # A Result can never exist without a preceding authorized intent, regardless
    # of whether the audit log is empty, truncated, or merely missing the entry.
    for t_entry in trace_entries:
        orphan_tx = t_entry.get("tx_id")
        if orphan_tx and orphan_tx not in audit_map:
            scanned_exit_codes.append(4)
            payload["uncommitted_tx_ids"].append(orphan_tx)
            payload["reason_details"][orphan_tx] = "RESULT_WITHOUT_INTENT"

    # Universal Aggregation Formula: ExitCode_final = max(runtime_event, max_scanned(chain_static))
    runtime_event_code = 4 if runtime_event_reason == "SAFELY_ABORTED_OPERATION" else 0
    max_static_code = max(scanned_exit_codes) if scanned_exit_codes else 0
    final_code = max(runtime_event_code, max_static_code)

    payload["exit_code"] = final_code
    if final_code == 4:
        payload["reason"] = "UNCOMMITTED_TRANSACTION"
    elif final_code == 2:
        payload["reason"] = "OFF_BOUNDARY_VIOLATION"
    elif final_code == 0:
        payload["reason"] = "SUCCESS"

    return final_code, payload


def main():
    parser = argparse.ArgumentParser(description="verify_runtime_trace v2.2.0 CLI")
    parser.add_argument("--trace", default="docs/delivery/execution-trace.json", help="Path to execution-trace.json")
    parser.add_argument(
        "--permission-log",
        default="docs/delivery/permission-audit.log",
        help="Path to permission-audit.log",
    )
    parser.add_argument("--task-pack", default="docs/delivery/tasks/TASK-001.md", help="Path to Task Pack Markdown")
    parser.add_argument(
        "--mode",
        default="goal",
        choices=["goal", "plan", "build"],
        help="Autonomy mode: goal, plan, build",
    )
    parser.add_argument("--next-iteration", type=int, default=1, help="Next iteration index k")
    parser.add_argument("--schemas", default="references/schemas.md", help="Path to schemas.md")
    parser.add_argument("--expansions", default="docs/delivery/expansions.json", help="Path to expansions.json")
    parser.add_argument("--runtime-event-reason", default=None, help="Runtime event reason string")
    parser.add_argument("--json", action="store_true", help="Output JSON payload")

    args = parser.parse_args()

    exit_code, payload = run_verification(
        trace_path=args.trace,
        log_path=args.permission_log,
        task_pack_path=args.task_pack,
        mode=args.mode,
        next_iteration=args.next_iteration,
        schemas_md_path=args.schemas,
        expansions_path=args.expansions,
        runtime_event_reason=args.runtime_event_reason
    )

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"[{payload['reason']}] Exit Code: {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
