#!/usr/bin/env python3
"""
Unit tests for lock_manager.py
"""

import os
import sys
import time
import shutil
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "codex-doc-first-development", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from lock_manager import LockManager, FileLockError


class TestLockManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.lock_file = os.path.join(self.temp_dir, ".log.lock")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_acquire_and_release(self):
        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        self.assertTrue(os.path.exists(self.lock_file))
        lm.release()
        self.assertFalse(os.path.exists(self.lock_file))

    def test_context_manager(self):
        with LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0) as lm:
            self.assertTrue(os.path.exists(self.lock_file))
        self.assertFalse(os.path.exists(self.lock_file))

    def test_stale_lock_recovery(self):
        # Create a stale lock with dead PID (-9999)
        with open(self.lock_file, "w", encoding="utf-8") as f:
            f.write('{"pid": -9999, "timestamp": 100000.0, "holder": "dead"}')

        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        lm.release()


if __name__ == "__main__":
    unittest.main()
