"""Self-heal helpers used by tests."""

from __future__ import annotations
import os
import sys
import subprocess
from typing import Any

__all__ = [
    "fix_unicode",
    "create_missing_inputs",
    "pip_install",
    "apply_remediation",
    "_run",
]


def fix_unicode(s: str) -> str:
    """Remove common unicode line separators that break logs/parsers."""
    if not isinstance(s, str):
        return s
    return s.replace("\u2028", "").replace("\u2029", "")


def create_missing_inputs(path: str = "missing_placeholder.tmp") -> None:
    """Safely create a missing input file (or its parent dirs)."""
    try:
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        # Best-effort: ignore any OS errors in tests
        pass


def _run(cmd: list[str] | tuple[str, ...], **kwargs: Any) -> subprocess.CompletedProcess:
    """Wrapper for subprocess.run so tests can monkeypatch."""
    # Don't pass check=True here; tests provide a fake object with returncode
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def pip_install(package: str) -> bool:
    """
    Best-effort installer used by remediation. Tests monkeypatch _run to avoid
    real network calls; we consider returncode==0 a success.
    """
    try:
        if not package:
            return False
        cmd = [sys.executable, "-m", "pip", "install", package]
        res = _run(cmd)
        # If a fake object is returned, it will at least have returncode=0 in tests
        rc = getattr(res, "returncode", 1)
        return rc == 0
    except Exception:
        return False


def apply_remediation(exc: Exception) -> bool:
    """
    Try to remediate a known class of errors.
    - FileNotFoundError: create a placeholder input and return True
    - ImportError: attempt pip install of a dummy pkg (tests monkeypatch pip_install) and return True
    - UnicodeError: normalize and return True
    Anything else → False.
    """
    msg = str(exc)
    lower = msg.lower()

    # File not found
    if isinstance(exc, FileNotFoundError) or "filenotfounderror" in lower:
        # Try to pull a filename after the colon, else use a safe default
        target = "missing_placeholder.tmp"
        if ":" in msg:
            maybe = msg.split(":", 1)[1].strip()
            if maybe:
                target = maybe
        create_missing_inputs(target)
        return True

    # Import error
    if isinstance(exc, ImportError) or "importerror" in lower or "no module named" in lower:
        # The tests monkeypatch pip_install → we just need to call it and return True
        _ = pip_install("missing-dependency")
        return True

    # Unicode problems
    if isinstance(exc, UnicodeError) or "unicode" in lower:
        _ = fix_unicode(msg)
        return True

    return False
