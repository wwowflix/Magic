"""
MAGIC shim module for ``scripts._iotools``.

This file exists so that tests/smoke/test_smoke_scripts__iotools.py
can import ``scripts._iotools`` without errors.

It provides a few tiny helpers that are safe no-ops for now.
If MAGIC ever needs richer behavior, you can extend this module.
"""

from __future__ import annotations

from typing import Iterable, List


class LineBuffer:
    """
    Very small line buffer abstraction.

    Stores lines of text and allows iteration. This is intentionally
    tiny and self-contained so that it is safe in the MAGIC environment.
    """

    def __init__(self, lines: Iterable[str] | None = None) -> None:
        self._lines: List[str] = list(lines or [])

    def add(self, line: str) -> None:
        """Append a single line of text."""
        self._lines.append(line)

    def __iter__(self):
        return iter(self._lines)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._lines)


def normalize_newlines(text: str) -> str:
    """
    Normalize CRLF / CR / LF sequences to ``\\n``.

    This is a generic helper that can be used by any future
    import/export utilities in MAGIC.
    """
    # First normalize Windows-style CRLF, then lone CR
    return text.replace("\\r\\n", "\\n").replace("\\r", "\\n")


__all__ = ["LineBuffer", "normalize_newlines"]
