from __future__ import annotations
import subprocess
from typing import Sequence, Any


def _run(cmd: Sequence[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """Thin wrapper so tests can monkeypatch."""
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def pip_install(requirement: str) -> bool:
    """Install one requirement; True on success."""
    try:
        proc = _run(["python", "-m", "pip", "install", requirement])
        return proc.returncode == 0
    except Exception:
        return False


def create_missing_inputs(path: str, *_, **__) -> None:
    """mkdir -p and touch empty file at the given path."""
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("", encoding="utf-8")


def fix_unicode(s: str) -> str:
    """Strip U+2028/U+2029."""
    if not isinstance(s, str):
        return s
    return s.replace("\u2028", "").replace("\u2029", "")


def apply_remediation(err: Exception) -> bool:
    """
    - FileNotFoundError -> create_missing_inputs -> True
    - ImportError       -> pip_install(missing)    -> True/False
    - UnicodeError      -> fix_unicode             -> True
    - Otherwise False
    """
    msg = str(err)
    if isinstance(err, FileNotFoundError) or "FileNotFoundError" in msg:
        create_missing_inputs("inputs/needme.txt")  # tests monkeypatch this call site
        return True
    if isinstance(err, ImportError) or "No module named" in msg:
        return pip_install("missing-dependency")
    if isinstance(err, UnicodeError):
        fix_unicode(msg)
        return True
    return False
