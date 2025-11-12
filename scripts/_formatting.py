"""
MAGIC-safe shim for scripts._formatting.

This module exists to make third-party formatting utilities safe to import
inside the MAGIC project. It avoids any dependency on vendor internals
or project-specific exception modules.

It provides:

- BaseExceptionGroup: a lightweight compatibility class
- format_exception(exc): string representation of a single exception
- format_exception_group(group): multi-line representation of an exception group
"""

from __future__ import annotations
from typing import Iterable, Sequence

# ---------------------------------------------------------------------------
# BaseExceptionGroup compatibility
# ---------------------------------------------------------------------------

try:
    _BaseExceptionGroup = BaseExceptionGroup  # type: ignore[name-defined]
except Exception:
    class _BaseExceptionGroup(Exception):
        """Minimal fallback BaseExceptionGroup for older interpreters."""
        def __init__(self, message: str, exceptions: Sequence[BaseException]):
            super().__init__(message)
            self.message = message
            self.exceptions = tuple(exceptions)
        def __repr__(self):
            return f"{self.__class__.__name__}({self.message!r}, {list(self.exceptions)!r})"

class BaseExceptionGroup(_BaseExceptionGroup):
    """Compatibility alias used inside MAGIC's scripts package."""
    pass

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_exception(exc: BaseException) -> str:
    """Return a simple one-line representation of an exception."""
    return f"{exc.__class__.__name__}: {exc}"

def format_exception_group(group: BaseExceptionGroup) -> str:
    """Return a multi-line representation of an exception group."""
    message = getattr(group, "message", str(group))
    exceptions: Iterable[BaseException] = getattr(group, "exceptions", ())
    lines = [f"{group.__class__.__name__}: {message}"]
    for index, exc in enumerate(exceptions, start=1):
        lines.append(f"  [{index}] {format_exception(exc)}")
    return "\n".join(lines)

__all__ = ["BaseExceptionGroup", "format_exception", "format_exception_group"]
