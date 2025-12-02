"""
MAGIC shim for scripts.errors.

This module provides a small subset of error classes modelled after
`rich.errors`, just enough for other MAGIC shims such as:

- scripts.style
- scripts.segment
- scripts.console
- scripts._inspect

The goal is:
- All imports of `scripts.errors` succeed
- Code that catches these exceptions still behaves sensibly
- We avoid heavy dependencies or complex logic here
"""

from __future__ import annotations

from typing import Optional


class ConsoleError(Exception):
    """Base error for MAGIC console / rich-style helpers."""


class StyleError(ConsoleError):
    """Raised when a style-related error occurs (bad style name, etc.)."""


class MarkupError(ConsoleError):
    """Raised when markup parsing or rendering fails."""


class MissingStyle(StyleError):
    """
    Raised when a requested style name cannot be found.

    This mirrors the behaviour of rich.errors.MissingStyle closely enough
    for tests and simple error handling.
    """

    def __init__(self, style: str, message: Optional[str] = None) -> None:
        msg = message or f"Unknown style: {style!r}"
        super().__init__(msg)
        self.style = style


__all__ = [
    "ConsoleError",
    "StyleError",
    "MarkupError",
    "MissingStyle",
    "Error",
    "ApproxNotFoundError",
]



# MAGIC shim: generic Error base used by some helpers
try:
    Error  # type: ignore[name-defined]
except NameError:
    class Error(Exception):
        """Generic MAGIC error base class used in stubs."""

        pass
class ApproxNotFoundError(Error):
    """
    MAGIC stub: raised when a curve approximation cannot be found.

    Only needed so that scripts.cu2qu / scripts.benchmark can import it.
    """
    pass
