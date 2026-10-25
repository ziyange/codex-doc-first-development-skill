#!/usr/bin/env python3
"""
lock_manager.py - Robust Advisory File Lock Manager

Provides cross-platform advisory file locking with PID and lease timeout validation,
supporting automatic stale lock recovery for crash-safe agent concurrency control.

Invariants:
- The OS-level advisory lock is always taken BEFORE any lock-file content is
  inspected or rewritten (never delete-then-lock, which races with waiters).
- release() clears the metadata while still holding the lock and never deletes
  the lock file, so every contender always races on the same inode.
- On Windows, acquire and release always address the same fixed byte range
  (byte 0, length 1) regardless of prior file size.
"""

import os
import sys
import time
import json
from typing import Optional

# Platform-specific locking primitives
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


class FileLockError(Exception):
    """Exception raised when lock acquisition fails or timed out."""
    pass


class LockManager:
    """
    Cross-platform file lock manager for docs/delivery/.log.lock.
    """

    def __init__(self, lock_file_path: str = "docs/delivery/.log.lock", timeout_seconds: float = 10.0, lease_ttl_seconds: float = 60.0):
        self.lock_file_path = lock_file_path
        self.timeout_seconds = timeout_seconds
        self.lease_ttl_seconds = lease_ttl_seconds
        self.file_obj: Optional[object] = None

    def _is_pid_alive(self, pid: int) -> bool:
        """Checks if a given PID is currently active on the host OS."""
        if pid <= 0:
            return False
        if sys.platform == "win32":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                SYNCHRONIZE = 0x00100000
                process = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
                if process != 0:
                    kernel32.CloseHandle(process)
                    return True
                return False
            except Exception:
                return True  # Defensive fallback
        else:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False

    def _clear_metadata(self):
        """Empties the lock file content in place (caller holds the OS lock)."""
        self.file_obj.seek(0)
        self.file_obj.truncate()
        self.file_obj.flush()

    def _clean_stale_lock(self):
        """
        Clears orphaned, expired, or corrupted metadata IN PLACE.

        Must only be called while holding the OS-level lock: rewriting (or, in
        the old design, deleting) the file without the lock raced with other
        waiters. The lock file itself is never removed, so every contender
        keeps racing on the same inode.
        """
        try:
            self.file_obj.seek(0)
            content = self.file_obj.read().strip()
        except OSError:
            return

        if not content:
            return

        try:
            data = json.loads(content)
            pid = data.get("pid", 0)
            timestamp = data.get("timestamp", 0)
            stale = (not self._is_pid_alive(pid)) or (time.time() - timestamp > self.lease_ttl_seconds)
        except (ValueError, AttributeError, TypeError):
            # Corrupted metadata: treat as stale and overwrite.
            stale = True

        if stale:
            self._clear_metadata()

    def _lock_os(self):
        """Applies the non-blocking OS advisory lock to a fixed byte range."""
        self.file_obj.seek(0)
        if sys.platform == "win32":
            msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _unlock_os(self):
        """Releases the OS advisory lock from the same fixed byte range."""
        self.file_obj.seek(0)
        if sys.platform == "win32":
            msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_UN)

    def acquire(self) -> bool:
        """
        Acquires the advisory lock, waiting up to timeout_seconds.
        """
        start_time = time.time()
        lock_dir = os.path.dirname(self.lock_file_path)
        if lock_dir and not os.path.exists(lock_dir):
            os.makedirs(lock_dir, exist_ok=True)

        while True:
            try:
                # Open without truncating: existing (possibly stale) content is
                # inspected and rewritten only after the OS lock is held.
                self.file_obj = open(self.lock_file_path, "a+", encoding="utf-8")

                # OS-level advisory lock first (fail-fast if another holder).
                self._lock_os()

                # Lock held: it is now safe to clear stale/corrupted metadata.
                self._clean_stale_lock()

                # Write PID and timestamp metadata
                self._clear_metadata()
                lock_info = {
                    "pid": os.getpid(),
                    "timestamp": time.time(),
                    "holder": "agent"
                }
                self.file_obj.write(json.dumps(lock_info))
                self.file_obj.flush()
                return True
            except OSError:
                if self.file_obj:
                    try:
                        self.file_obj.close()
                    except OSError:
                        pass
                    self.file_obj = None

                if time.time() - start_time >= self.timeout_seconds:
                    raise FileLockError(f"Could not acquire lock on {self.lock_file_path} within {self.timeout_seconds}s")

                time.sleep(0.1)

    def release(self):
        """
        Releases the advisory lock and clears the metadata.

        The lock file is intentionally kept (never unlinked): deleting a locked
        file lets a late opener lock a deleted inode while a third process
        creates and locks a fresh file, producing two simultaneous "holders".
        """
        if self.file_obj:
            try:
                # Clear metadata BEFORE releasing the OS lock, so no other
                # holder can write between our truncate and the unlock.
                self._clear_metadata()
                self._unlock_os()
                self.file_obj.close()
            except OSError:
                pass
            finally:
                self.file_obj = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
