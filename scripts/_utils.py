# -*- coding: utf-8 -*-
"""Utility shims for scripts package (MAGIC Week 6 Step 6.2)."""

from __future__ import annotations
from typing import Optional, Any
__all__ = ["peek_filelike_length", "primitive_value_to_str", 'extract_error_code', 'extract_err_message', 'NoLock']

def peek_filelike_length(f) -> Optional[int]:
    """Return remaining length for a seekable file-like object, or None.

    Uses tell/seek. Restores the original position.
    """
    try:
        pos = f.tell()
    except Exception:
        return None
    end = pos
    try:
        f.seek(0, 2)  # SEEK_END
        end = f.tell()
    except Exception:
        try:
            f.seek(pos)
        except Exception:
            pass
        return None
    finally:
        try:
            f.seek(pos)
        except Exception:
            pass
    try:
        remaining = end - pos
        return remaining if remaining >= 0 else 0
    except Exception:
        return None

def primitive_value_to_str(value: Any) -> str:
    """Convert primitives/bytes to safe str for HTTP parameters/headers."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8", "replace")
        except Exception:
            return str(value)
    try:
        return str(value)
    except Exception:
        return ""

def extract_error_code(exc) -> int | None:
    """Best-effort errno extraction from socket/OS/SSL errors."""
    try:
        # Common spots: .errno or first arg
        if hasattr(exc, "errno") and exc.errno is not None:
            return exc.errno
        if getattr(exc, "args", None):
            arg0 = exc.args[0]
            if isinstance(arg0, tuple) and arg0:
                # e.g., (errno, message)
                if isinstance(arg0[0], int):
                    return arg0[0]
            if isinstance(arg0, int):
                return arg0
    except Exception:
        pass
    return None
def extract_err_message(exc) -> str:
    """Best-effort human message for socket/SSL errors."""
    try:
        if getattr(exc, "strerror", None):
            return str(exc.strerror)
        if getattr(exc, "args", None):
            if len(exc.args) == 2 and isinstance(exc.args[1], str):
                return exc.args[1]
            if exc.args:
                return str(exc.args[0])
    except Exception:
        pass
    try:
        return str(exc)
    except Exception:
        return ""
class NoLock:
    """No-op lock/context used by websocket core."""
    def acquire(self, *args, **kwargs):
        return True
    def release(self):
        return None
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        # don't suppress exceptions
        return False
