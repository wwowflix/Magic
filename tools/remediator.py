from __future__ import annotations
import subprocess
import sys
import os
from typing import Any, Sequence

__all__ = ["fix_unicode", "create_missing_inputs", "pip_install", "apply_remediation", "_run"]

def fix_unicode(s: str) -> str:
    """Remove common Unicode line separators that break logs/parsers."""
    if not isinstance(s, str):
        return s
    return s.replace("\u2028", "").replace("\u2029", "")

def create_missing_inputs(path: str = "missing_placeholder.tmp") -> None:
    """Safely create a missing input file (and its parent dirs)."""
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "a", encoding="utf-8"):
            pass

def pip_install(pkgs: Sequence[str]) -> int:
    """Attempt to install missing packages; return subprocess exit code."""
    if not pkgs:
        return 0
    args = [sys.executable, "-m", "pip", "install", *pkgs]
    return subprocess.call(args)

def _run(cmd: Sequence[str]) -> int:
    """Run a command and return exit code (tiny wrapper to stub in tests)."""
    return subprocess.call(list(cmd))

def apply_remediation(err: BaseException) -> str:
    """
    Decide a remediation label for a given exception (toy example for unit tests).
    Return a short string tag describing what we’d do.
    """
    msg = str(err)
    if "No module named" in msg:
        return "pip_install_missing"
    if isinstance(err, FileNotFoundError):
        return "create_missing_input"
    if "UnicodeEncodeError" in msg or "line separator" in msg:
        return "fix_unicode"
    return "noop"
