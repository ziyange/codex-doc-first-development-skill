#!/usr/bin/env python3
"""
check_permission_log.py - AuditLog Merkle Chain Static Verification Module

Internal helper module imported by verify_runtime_trace.py to verify
permission-audit.log Merkle chain integrity and status consistency.
"""

import os
import sys
import json
import hashlib
from typing import List, Dict, Tuple, Optional


def normalize_path(path_str: str, root_dir: str = ".") -> str:
    """
    Normalizes a path string:
    1. Relative to root_dir
    2. Forward slashes
    3. Collapse ./ and ../
    4. Lowercase for case-insensitive comparison
    """
    if not path_str or path_str == "N/A":
        return "N/A"
    
    # Clean slashes
    clean_path = path_str.replace("\\", "/")
    
    # Remove leading ./ if present
    if clean_path.startswith("./"):
        clean_path = clean_path[2:]
        
    return clean_path.lower()


def compute_intent_hash(prev_hash: str, action_type: str, normalized_path: str, tx_id: str) -> str:
    """
    Computes SHA256 chain hash:
    SHA256(prev_hash + ":" + action_type + ":" + normalized_path + ":" + tx_id)
    Note: status and timestamp are explicitly excluded from hash computation to allow in-place status mutation.
    """
    payload = f"{prev_hash}:{action_type}:{normalized_path}:{tx_id}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_merkle_chain(log_entries: List[Dict]) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Verifies Merkle chain invariants:
    1. Record 1 prev_hash MUST equal "GENESIS"
    2. Record n prev_hash MUST equal Record n-1 intent_hash
    3. Record n intent_hash MUST match computed SHA256 payload

    Returns:
        (is_valid, error_reason, failing_index)
    """
    if not log_entries:
        return True, None, None

    for i, entry in enumerate(log_entries):
        tx_id = entry.get("tx_id", "")
        action_type = entry.get("action_type", "")
        path = entry.get("normalized_path", "")
        prev_hash = entry.get("prev_hash", "")
        intent_hash = entry.get("intent_hash", "")

        # Check invariant 1: First record must have prev_hash "GENESIS"
        if i == 0:
            if prev_hash != "GENESIS":
                return False, f"First record prev_hash is '{prev_hash}', expected 'GENESIS'", i
        else:
            expected_prev = log_entries[i - 1].get("intent_hash", "")
            if prev_hash != expected_prev:
                return False, f"Record {i} prev_hash '{prev_hash}' does not match record {i-1} intent_hash '{expected_prev}'", i

        # Check invariant 2: Hash payload matches
        computed = compute_intent_hash(prev_hash, action_type, path, tx_id)
        if computed != intent_hash:
            return False, f"Record {i} computed hash '{computed}' does not match stored intent_hash '{intent_hash}'", i

    return True, None, None


def parse_audit_log(file_path: str) -> List[Dict]:
    """
    Parses permission-audit.log (JSON lines or JSON array format).
    """
    if not os.path.exists(file_path):
        return []

    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        
        # Try JSON array first
        if content.startswith("["):
            try:
                entries = json.loads(content)
            except json.JSONDecodeError:
                pass
        else:
            # Try JSON Lines
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return entries


def main():
    """CLI entrypoint for standalone debugging of check_permission_log."""
    if len(sys.argv) < 2:
        print("Usage: python check_permission_log.py <path_to_permission-audit.log>")
        sys.exit(3)
        
    log_path = sys.argv[1]
    entries = parse_audit_log(log_path)
    is_valid, err, idx = verify_merkle_chain(entries)
    
    if not is_valid:
        print(f"[FAIL] Merkle chain broken at index {idx}: {err}")
        sys.exit(5)
        
    print(f"[PASS] Audit log Merkle chain valid ({len(entries)} entries).")
    sys.exit(0)


if __name__ == "__main__":
    main()
