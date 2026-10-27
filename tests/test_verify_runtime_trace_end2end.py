#!/usr/bin/env python3
"""
End-to-End Integration Tests for verify_runtime_trace.py against fixtures.
"""

import os
import sys
import json
import subprocess
import unittest
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "codex-doc-first-development", "scripts")
VERIFY_SCRIPT = os.path.join(SCRIPTS_DIR, "verify_runtime_trace.py")
FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")


class TestVerifyRuntimeTraceEnd2End(unittest.TestCase):
    def test_missing_project_inputs_return_structured_exit_3(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, VERIFY_SCRIPT, "--json"]
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["reason"], "SCHEMA_OR_PARSE_FAILURE")
            self.assertNotIn("Traceback", result.stderr)

    def test_installed_cli_uses_bundled_schemas_from_project_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, VERIFY_SCRIPT,
                       "--trace", os.path.join(FIXTURES_DIR, "valid_trace.json"),
                       "--permission-log", os.path.join(FIXTURES_DIR, "valid_audit.log"),
                       "--task-pack", os.path.join(FIXTURES_DIR, "valid_task_pack.md"),
                       "--json"]
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["reason"], "SUCCESS")

            command.extend(["--schemas", os.path.join(directory, "missing.md")])
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)

    def setUp(self):
        self.valid_task_pack = os.path.join(FIXTURES_DIR, "valid_task_pack.md")
        self.valid_audit = os.path.join(FIXTURES_DIR, "valid_audit.log")
        self.valid_trace = os.path.join(FIXTURES_DIR, "valid_trace.json")
        self.tampered_audit = os.path.join(FIXTURES_DIR, "tampered_merkle_audit.log")
        self.unauthorized_audit = os.path.join(FIXTURES_DIR, "unauthorized_audit.log")
        self.unauthorized_trace = os.path.join(FIXTURES_DIR, "unauthorized_write_trace.json")

    def run_cli(self, trace_path, audit_path, task_pack_path, mode="goal", next_iteration=1):
        schemas_path = os.path.join(REPO_ROOT, "codex-doc-first-development", "references", "schemas.md")
        cmd = [
            sys.executable,
            VERIFY_SCRIPT,
            "--trace", trace_path,
            "--permission-log", audit_path,
            "--task-pack", task_pack_path,
            "--schemas", schemas_path,
            "--mode", mode,
            "--next-iteration", str(next_iteration),
            "--json"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        try:
            payload = json.loads(result.stdout) if result.stdout else {}
        except json.JSONDecodeError:
            payload = {}
        return result.returncode, payload

    def test_valid_fixtures_pass_with_exit_code_0(self):
        code, payload = self.run_cli(self.valid_trace, self.valid_audit, self.valid_task_pack)
        self.assertEqual(code, 0)
        self.assertEqual(payload.get("reason"), "SUCCESS")
        self.assertEqual(payload.get("exit_code"), 0)

    def test_tampered_merkle_log_triggers_exit_code_5(self):
        code, payload = self.run_cli(self.valid_trace, self.tampered_audit, self.valid_task_pack)
        self.assertEqual(code, 5)
        self.assertEqual(payload.get("reason"), "TAMPER_OR_HASH_MISMATCH")
        self.assertEqual(payload.get("exit_code"), 5)

    def test_unauthorized_write_triggers_exit_code_2(self):
        code, payload = self.run_cli(self.unauthorized_trace, self.unauthorized_audit, self.valid_task_pack)
        self.assertEqual(code, 2)
        self.assertEqual(payload.get("reason"), "OFF_BOUNDARY_VIOLATION")
        self.assertEqual(payload.get("exit_code"), 2)


if __name__ == "__main__":
    unittest.main()
