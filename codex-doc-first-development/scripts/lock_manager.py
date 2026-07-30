#!/usr/bin/env python3
"""
lock_manager.py - Robust Advisory File Lock Manager

Provides cross-platform advisory file locking with PID and lease timeout validation,
supporting automatic stale lock recovery for crash-safe agent concurrency control.
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

    def _clean_stale_lock(self):
        """Removes lock file if it is orphaned or expired."""
        if not os.path.exists(self.lock_file_path):
            return

        try:
            with open(self.lock_file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    pid = data.get("pid", 0)
                    timestamp = data.get("timestamp", 0)

                    # Check if process is dead or lease is expired
                    if not self._is_pid_alive(pid) or (time.time() - timestamp > self.lease_ttl_seconds):
                        os.remove(self.lock_file_path)
                        return
        except Exception:
            # If corrupted, clear stale lock safely
            try:
                os.remove(self.lock_file_path)
            except OSError:
                pass

    def acquire(self) -> bool:
        """
        Acquires the advisory lock, waiting up to timeout_seconds.
        """
        start_time = time.time()
        lock_dir = os.path.dirname(self.lock_file_path)
        if lock_dir and not os.path.exists(lock_dir):
            os.makedirs(lock_dir, exist_ok=True)

        while True:
            # First attempt stale lock recovery
            self._clean_stale_lock()

            try:
                self.file_obj = open(self.lock_file_path, "a+", encoding="utf-8")
                
                # Apply OS-level advisory lock
                if sys.platform == "win32":
                    msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Write PID and timestamp metadata
                self.file_obj.seek(0)
                self.file_obj.truncate()
                lock_info = {
                    "pid": os.getpid(),
                    "timestamp": time.time(),
                    "holder": "agent"
                }
                self.file_obj.write(json.dumps(lock_info))
                self.file_obj.flush()
                return True
            except (OSError, IOError, Exception):
                if self.file_obj:
                    try:
                        self.file_obj.close()
                    except Exception:
                        pass
                    self.file_obj = None

                if time.time() - start_time >= self.timeout_seconds:
                    raise FileLockError(f"Could not acquire lock on {self.lock_file_path} within {self.timeout_seconds}s")
                
                time.sleep(0.1)

    def release(self):
        """Releases the advisory lock and removes lockfile."""
        if self.file_obj:
            try:
                if sys.platform == "win32":
                    self.file_obj.seek(0)
                    msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_UN)
                self.file_obj.close()
            except Exception:
                pass
            finally:
                self.file_obj = None

            try:
                if os.path.exists(self.lock_file_path):
                    os.remove(self.lock_file_path)
            except OSError:
                pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
