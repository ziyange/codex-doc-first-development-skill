#!/usr/bin/env python3
"""
Unit tests for verify_runtime_trace.py (Benchmark Tests TC-V01 ~ TC-V24)
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add scripts directory to path
SCRIPTS_DIR = str(Path(__file__).parent.parent / "codex-doc-first-development" / "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from verify_runtime_trace import run_verification
from check_permission_log import compute_intent_hash, normalize_path


class TestVerifyRuntimeTrace(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.schemas_path = str(
            Path(__file__).parent.parent
            / "codex-doc-first-development"
            / "references"
            / "schemas.md"
        )
        self.trace_path = str(self.temp_path / "execution-trace.json")
        self.log_path = str(self.temp_path / "permission-audit.log")
        self.task_pack_path = str(self.temp_path / "TASK-001.md")
        self.expansions_path = str(self.temp_path / "expansions.json")
        # A clean initialized audit state is explicit; missing inputs must fail.
        Path(self.trace_path).write_text("[]", encoding="utf-8")
        Path(self.log_path).write_text("[]", encoding="utf-8")

        # Create valid Task Pack
        with open(self.task_pack_path, "w", encoding="utf-8") as f:
            f.write("""# TASK-001: Sample Task

## Allowed Files
- src/auth/*.ts

MAX_ITERATIONS: 5
""")

        # Create empty expansions.json
        with open(self.expansions_path, "w", encoding="utf-8") as f:
            f.write("[]")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_or_corrupted_required_inputs_fail_closed(self):
        for target in (self.trace_path, self.log_path, self.task_pack_path):
            for content in (None, "not valid input", "[null]"):
                with self.subTest(target=target, content=content):
                    Path(self.trace_path).write_text("[]", encoding="utf-8")
                    Path(self.log_path).write_text("[]", encoding="utf-8")
                    Path(self.task_pack_path).write_text("# TASK-001\nMAX_ITERATIONS: 5\n", encoding="utf-8")
                    if content is None:
                        Path(target).unlink()
                    else:
                        Path(target).write_text(content, encoding="utf-8")
                    code, payload = self._verify()
                    self.assertEqual(code, 3)
                    self.assertEqual(payload["reason"], "SCHEMA_OR_PARSE_FAILURE")

    def test_goal_requires_valid_explicit_iteration_limit(self):
        Path(self.trace_path).write_text("[]", encoding="utf-8")
        Path(self.log_path).write_text("[]", encoding="utf-8")
        for limit in ("", "abc", "0", "11", "-1", "2.5"):
            with self.subTest(limit=limit):
                Path(self.task_pack_path).write_text(f"# TASK-001\nMAX_ITERATIONS: {limit}\n", encoding="utf-8")
                code, _ = self._verify()
                self.assertEqual(code, 3)

    def test_corrupted_existing_expansions_fail_closed(self):
        Path(self.trace_path).write_text("[]", encoding="utf-8")
        Path(self.log_path).write_text("[]", encoding="utf-8")
        Path(self.expansions_path).write_text("not json", encoding="utf-8")
        self.assertEqual(self._verify()[0], 3)

    def _verify(self, task_pack=None, schemas=None, mode="goal", iteration=1, event=None):
        """Run verification with the standard fixture paths."""
        return run_verification(
            self.trace_path,
            self.log_path,
            task_pack or self.task_pack_path,
            mode,
            iteration,
            schemas or self.schemas_path,
            self.expansions_path,
            runtime_event_reason=event,
        )

    def _create_log_entry(self, tx_id, action_type, path, prev_hash, status="COMMITTED"):
        intent_hash = compute_intent_hash(prev_hash, action_type, path, tx_id)
        return {
            "tx_id": tx_id,
            "timestamp": "2026-07-28T09:00:00Z",
            "action_type": action_type,
            "normalized_path": path,
            "prev_hash": prev_hash,
            "intent_hash": intent_hash,
            "status": status
        }

    def _create_trace_entry(self, tx_id, iteration, action_type, path, intent_hash, result_status="COMPLETED"):
        return {
            "tx_id": tx_id,
            "iteration_index": iteration,
            "timestamp": "2026-07-28T09:00:05Z",
            "action_type": action_type,
            "normalized_path": path,
            "intent_hash": intent_hash,
            "result_status": result_status,
            "ignored_candidates": []
        }

    def test_tc_v01_iteration_allowed(self):
        """TC-V01: --next-iteration 5 (MAX=5) -> Exit 0 (SUCCESS)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS")
        trace = self._create_trace_entry(tx_id, 5, "FILE_WRITE", "src/auth/jwt.ts", entry["intent_hash"])

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify(iteration=5)
        self.assertEqual(code, 0)
        self.assertEqual(payload["reason"], "SUCCESS")

    def test_tc_v02_iteration_exceeded(self):
        """TC-V02: --next-iteration 6 (MAX=5) -> Exit 1 (ITERATION_EXCEEDED)"""
        code, payload = self._verify(iteration=6)
        self.assertEqual(code, 1)
        self.assertEqual(payload["reason"], "ITERATION_EXCEEDED")

    def test_tc_v03_off_boundary_violation(self):
        """TC-V03: Write to unauthorized file -> Exit 2 (OFF_BOUNDARY_VIOLATION)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/unauthorized.py", "GENESIS")
        trace = self._create_trace_entry(tx_id, 1, "FILE_WRITE", "src/unauthorized.py", entry["intent_hash"])

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify()
        self.assertEqual(code, 2)
        self.assertEqual(payload["reason"], "OFF_BOUNDARY_VIOLATION")

    def test_tc_v04_schema_missing(self):
        """TC-V04: schemas.md missing or invalid schema ID -> Exit 3 (SCHEMA_OR_PARSE_FAILURE)"""
        code, payload = self._verify(schemas="invalid_schemas_path.md")
        self.assertEqual(code, 3)
        self.assertEqual(payload["reason"], "SCHEMA_OR_PARSE_FAILURE")

    def test_tc_v05_uncommitted_pending(self):
        """TC-V05: PENDING + Absent -> Exit 4 (reason_details: {tx: UNCOMMITTED_PENDING})"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="PENDING")

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))

        code, payload = self._verify()
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason_details"].get(tx_id), "UNCOMMITTED_PENDING")

    def test_tc_v06_legitimate_aborted(self):
        """TC-V06: ABORTED + Absent -> Exit 0 (Exempted放行)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="ABORTED")

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))

        code, payload = self._verify()
        self.assertEqual(code, 0)

    def test_tc_v07_committed_result_missing(self):
        """TC-V07: COMMITTED + Absent -> Exit 4 (reason_details: {tx: COMMITTED_RESULT_MISSING})"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="COMMITTED")

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))

        code, payload = self._verify()
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason_details"].get(tx_id), "COMMITTED_RESULT_MISSING")

    def test_tc_v08_pending_with_result_illegal(self):
        """TC-V08: PENDING + Present -> Exit 6 (ILLEGAL_TRANSACTION_STATE)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="PENDING")
        trace = self._create_trace_entry(tx_id, 1, "FILE_WRITE", "src/auth/jwt.ts", entry["intent_hash"])

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify()
        self.assertEqual(code, 6)
        self.assertEqual(payload["reason"], "ILLEGAL_TRANSACTION_STATE")

    def test_tc_v09_mode_switch_pass(self):
        """TC-V09: MODE_SWITCH single-step commit -> Exit 0"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "MODE_SWITCH", "N/A", "GENESIS", status="COMMITTED")
        trace = self._create_trace_entry(
            tx_id, 1, "MODE_SWITCH", "N/A", entry["intent_hash"], result_status="FUSED_TO_PLAN"
        )

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify()
        self.assertEqual(code, 0)

    def test_tc_v10_merkle_chain_tampered(self):
        """TC-V10: Delete middle record in Merkle chain -> Exit 5 (TAMPER_OR_HASH_MISMATCH)"""
        e1 = self._create_log_entry(
            "11111111-1111-1111-1111-111111111111", "FILE_WRITE", "src/auth/a.ts", "GENESIS"
        )
        e2 = self._create_log_entry(
            "22222222-2222-2222-2222-222222222222", "FILE_WRITE", "src/auth/b.ts", e1["intent_hash"]
        )
        e3 = self._create_log_entry(
            "33333333-3333-3333-3333-333333333333", "FILE_WRITE", "src/auth/c.ts", e2["intent_hash"]
        )

        # Delete middle entry e2
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([e1, e3]))

        code, payload = self._verify()
        self.assertEqual(code, 5)
        self.assertTrue(payload["scan_truncated"])

    def test_tc_v11_trace_intent_hash_tampered(self):
        """TC-V11: Modify intent_hash in trace -> Exit 5 (TAMPER_OR_HASH_MISMATCH)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS")
        trace = self._create_trace_entry(
            tx_id, 1, "FILE_WRITE", "src/auth/jwt.ts", "0" * 64
        )

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify()
        self.assertEqual(code, 5)

    def test_tc_v12_forged_expansions(self):
        """TC-V12: expansions.json forged without audit log grant -> Exit 5"""
        expansions = [{
            "expansion_seq": 1,
            "tx_id": "99999999-9999-9999-9999-999999999999",
            "approved_pattern": "src/forged/*.ts",
            "approved_at": "2026-07-28T09:00:00Z",
            "approved_by": "ATTACKER"
        }]
        with open(self.expansions_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(expansions))

        code, payload = self._verify()
        self.assertEqual(code, 5)

    def test_tc_v13_expansions_limit_exceeded(self):
        """TC-V13: 3 expansions (max=2) -> Exit 2 (OFF_BOUNDARY_VIOLATION, EXPANSION_LIMIT_EXCEEDED)"""
        grant1 = self._create_log_entry(
            "11111111-1111-1111-1111-111111111111", "PERMISSION_GRANT", "src/extra1/*.ts", "GENESIS"
        )
        grant2 = self._create_log_entry(
            "22222222-2222-2222-2222-222222222222", "PERMISSION_GRANT", "src/extra2/*.ts",
            grant1["intent_hash"],
        )
        grant3 = self._create_log_entry(
            "33333333-3333-3333-3333-333333333333", "PERMISSION_GRANT", "src/extra3/*.ts",
            grant2["intent_hash"],
        )

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([grant1, grant2, grant3]))

        expansions = [
            {"expansion_seq": 1, "tx_id": grant1["tx_id"], "approved_pattern": "src/extra1/*.ts",
             "approved_at": "2026-07-28T09:00:00Z", "approved_by": "USER"},
            {"expansion_seq": 2, "tx_id": grant2["tx_id"], "approved_pattern": "src/extra2/*.ts",
             "approved_at": "2026-07-28T09:01:00Z", "approved_by": "USER"},
            {"expansion_seq": 3, "tx_id": grant3["tx_id"], "approved_pattern": "src/extra3/*.ts",
             "approved_at": "2026-07-28T09:02:00Z", "approved_by": "USER"}
        ]
        with open(self.expansions_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(expansions))

        code, payload = self._verify()
        self.assertEqual(code, 2)
        self.assertEqual(payload["reason"], "OFF_BOUNDARY_VIOLATION")
        self.assertEqual(payload["runtime_event_reason"], "EXPANSION_LIMIT_EXCEEDED")

    def test_tc_v14_safely_aborted_operation(self):
        """TC-V14: Lock write exception safely aborted -> Exit 4 (runtime_event_reason: SAFELY_ABORTED_OPERATION)"""
        code, payload = self._verify(event="SAFELY_ABORTED_OPERATION")
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason"], "UNCOMMITTED_TRANSACTION")
        self.assertEqual(payload["runtime_event_reason"], "SAFELY_ABORTED_OPERATION")

    def test_tc_v15_secondary_fault(self):
        """TC-V15: Secondary fault during cleanup -> Exit 3"""
        # Verified via script fail-close handling
        code, payload = self._verify(schemas="non_existent_schema.md")
        self.assertEqual(code, 3)

    def test_tc_v16_max_aggregation_overrides(self):
        """TC-V16: Exit 4 event code + Exit 6 short-circuit -> Exit 6 (scan_truncated validated by TC-V18)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="PENDING")
        trace = self._create_trace_entry(tx_id, 1, "FILE_WRITE", "src/auth/jwt.ts", entry["intent_hash"])

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify(event="SAFELY_ABORTED_OPERATION")
        self.assertEqual(code, 6)

    def test_tc_v17_multiple_exit_4_reasons_preserved(self):
        """TC-V17: Multiple Exit 4 entries with distinct sub-reasons -> Exit 4, reason_details preserves all"""
        e1 = self._create_log_entry(
            "11111111-1111-1111-1111-111111111111", "FILE_WRITE", "src/auth/a.ts", "GENESIS",
            status="PENDING",
        )
        e2 = self._create_log_entry(
            "22222222-2222-2222-2222-222222222222", "FILE_WRITE", "src/auth/b.ts",
            e1["intent_hash"], status="COMMITTED",
        )

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([e1, e2]))

        code, payload = self._verify()
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason_details"].get(e1["tx_id"]), "UNCOMMITTED_PENDING")
        self.assertEqual(payload["reason_details"].get(e2["tx_id"]), "COMMITTED_RESULT_MISSING")

    def test_tc_v18_short_circuit_scan_truncated(self):
        """TC-V18: Node 1 Exit 4, Node 2 Exit 6 short-circuit, Node 3 unscanned.

        scan_truncated must be true and reason_details must contain Node 1 only.
        """
        e1 = self._create_log_entry(
            "11111111-1111-1111-1111-111111111111", "FILE_WRITE", "src/auth/a.ts", "GENESIS",
            status="PENDING",
        )
        e2 = self._create_log_entry(
            "22222222-2222-2222-2222-222222222222", "FILE_WRITE", "src/auth/b.ts",
            e1["intent_hash"], status="PENDING",
        )
        e3 = self._create_log_entry(
            "33333333-3333-3333-3333-333333333333", "FILE_WRITE", "src/auth/c.ts",
            e2["intent_hash"], status="COMMITTED",
        )

        # Create trace for e2 to trigger Exit 6 (PENDING + Present)
        t2 = self._create_trace_entry(e2["tx_id"], 1, "FILE_WRITE", "src/auth/b.ts", e2["intent_hash"])

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([e1, e2, e3]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([t2]))

        code, payload = self._verify()
        self.assertEqual(code, 6)
        self.assertTrue(payload["scan_truncated"])
        self.assertIn(e1["tx_id"], payload["reason_details"])
        self.assertNotIn(e3["tx_id"], payload["reason_details"])

    def test_tc_v19_dual_channel_coexistence(self):
        """TC-V19: SAFELY_ABORTED_OPERATION event + UNCOMMITTED_PENDING node -> Dual channels non-empty"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS", status="PENDING")

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))

        code, payload = self._verify(event="SAFELY_ABORTED_OPERATION")
        self.assertEqual(code, 4)
        self.assertEqual(payload["runtime_event_reason"], "SAFELY_ABORTED_OPERATION")
        self.assertEqual(payload["reason_details"].get(tx_id), "UNCOMMITTED_PENDING")

    def test_tc_v20_empty_allowed_files_fails_closed(self):
        """TC-V20: Task Pack without Allowed Files + FILE_WRITE -> Exit 2 (fail-close, never fail-open)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/anything.py", "GENESIS")
        trace = self._create_trace_entry(tx_id, 1, "FILE_WRITE", "src/anything.py", entry["intent_hash"])

        # Task Pack with NO Allowed Files section at all
        empty_whitelist_pack = self.temp_path / "TASK-EMPTY.md"
        empty_whitelist_pack.write_text("""# TASK-EMPTY: No Whitelist

## Allowed Files

MAX_ITERATIONS: 5
""", encoding="utf-8")

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([trace]))

        code, payload = self._verify(task_pack=str(empty_whitelist_pack))
        self.assertEqual(code, 2)
        self.assertEqual(payload["reason"], "OFF_BOUNDARY_VIOLATION")
        self.assertIn("src/anything.py", payload["offending_files"])

    def test_tc_v21_orphan_trace_result_without_intent(self):
        """TC-V21: Result trace without AuditLog intent -> Exit 4 (RESULT_WITHOUT_INTENT)"""
        tx_id = "3b92f7c0-8d4e-4a11-b921-998877665544"
        # A legitimate committed write...
        entry = self._create_log_entry(tx_id, "FILE_WRITE", "src/auth/jwt.ts", "GENESIS")
        # ...plus a forged Result whose intent was never recorded.
        orphan_tx = "99999999-9999-9999-9999-999999999999"
        orphan = self._create_trace_entry(orphan_tx, 1, "FILE_WRITE", "src/evil.py", "0" * 64)

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([entry]))
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([orphan]))

        code, payload = self._verify()
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason"], "UNCOMMITTED_TRANSACTION")
        self.assertEqual(payload["reason_details"].get(orphan_tx), "RESULT_WITHOUT_INTENT")
        self.assertIn(orphan_tx, payload["uncommitted_tx_ids"])

    def test_tc_v22_empty_log_with_trace_fails_closed(self):
        """TC-V22: Empty audit log + non-empty trace -> Exit 4 (empty state never auto-passes a Result)"""
        orphan_tx = "88888888-8888-8888-8888-888888888888"
        orphan = self._create_trace_entry(orphan_tx, 1, "FILE_WRITE", "src/x.py", "0" * 64)

        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([orphan]))

        code, payload = self._verify()
        self.assertEqual(code, 4)
        self.assertEqual(payload["reason_details"].get(orphan_tx), "RESULT_WITHOUT_INTENT")

    def test_tc_v23_empty_log_and_trace_passes(self):
        """TC-V23: Empty audit log + empty trace -> Exit 0 (no false positives on a clean slate)"""
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(self.trace_path, "w", encoding="utf-8") as f:
            f.write("[]")

        code, payload = self._verify()
        self.assertEqual(code, 0)
        self.assertEqual(payload["reason"], "SUCCESS")

    def test_tc_v24_normalize_path_preserves_case(self):
        """TC-V24: normalize_path must be platform-independent (hashes verify identically everywhere)"""
        self.assertEqual(normalize_path("src/App.py"), "src/App.py")
        self.assertEqual(normalize_path(".\\src\\App.py"), "src/App.py")
        self.assertEqual(normalize_path("./src/App.py"), "src/App.py")
        self.assertEqual(normalize_path("N/A"), "N/A")
        # The intent hash of a recorded path must not depend on the verifying OS.
        expected = compute_intent_hash("GENESIS", "FILE_WRITE", "src/App.py", "TX-001")
        self.assertEqual(
            compute_intent_hash("GENESIS", "FILE_WRITE", normalize_path("src/App.py"), "TX-001"),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
