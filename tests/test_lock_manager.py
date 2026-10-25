#!/usr/bin/env python3
"""
Unit tests for lock_manager.py
"""
import os
import sys
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

    def _read_lock_content(self, holder: "LockManager | None" = None) -> str:
        """
        Reads the lock file content.

        While a lock is held, reads go through the holder's own file handle:
        on Windows, msvcrt-locked byte ranges reject reads from other handles,
        which is intended - no contender ever needs to read the content
        without holding the lock.
        """
        if holder is not None and holder.file_obj is not None:
            holder.file_obj.seek(0)
            return holder.file_obj.read()
        with open(self.lock_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_acquire_and_release(self):
        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        self.assertTrue(os.path.exists(self.lock_file))
        self.assertIn("pid", self._read_lock_content(lm))
        lm.release()
        # The lock file is kept by design (never unlinked while locked);
        # its metadata is cleared so the next contender sees an empty file.
        self.assertTrue(os.path.exists(self.lock_file))
        self.assertEqual(self._read_lock_content().strip(), "")

    def test_reacquire_after_release(self):
        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        lm.release()
        # A second manager can immediately re-acquire the same lock file.
        lm2 = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm2.acquire())
        self.assertIn("pid", self._read_lock_content(lm2))
        lm2.release()

    def test_context_manager(self):
        with LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0) as lm:
            self.assertTrue(os.path.exists(self.lock_file))
            self.assertIn("pid", self._read_lock_content(lm))
        self.assertTrue(os.path.exists(self.lock_file))
        self.assertEqual(self._read_lock_content().strip(), "")

    def test_stale_lock_recovery(self):
        # Create a stale lock with dead PID (-9999)
        with open(self.lock_file, "w", encoding="utf-8") as f:
            f.write('{"pid": -9999, "timestamp": 100000.0, "holder": "dead"}')

        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        # Stale metadata was overwritten in place with our own PID.
        self.assertIn(str(os.getpid()), self._read_lock_content(lm))
        lm.release()

    def test_corrupted_lock_is_taken_over(self):
        # Corrupted (non-JSON) content must not block acquisition.
        with open(self.lock_file, "w", encoding="utf-8") as f:
            f.write("not json at all <<<")

        lm = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(lm.acquire())
        self.assertIn(str(os.getpid()), self._read_lock_content(lm))
        lm.release()

    def test_held_lock_times_out_for_others(self):
        holder = LockManager(lock_file_path=self.lock_file, timeout_seconds=1.0)
        self.assertTrue(holder.acquire())

        contender = LockManager(lock_file_path=self.lock_file, timeout_seconds=0.3)
        with self.assertRaises(FileLockError):
            contender.acquire()

        # The holder's metadata is untouched by the failed contender.
        self.assertIn(str(os.getpid()), self._read_lock_content(holder))
        holder.release()


if __name__ == "__main__":
    unittest.main()
