"""
MAGIC shim for scripts.pretty.

Goal:
- Provide a `Pretty` object that can be imported by scripts._inspect
- Prefer the real Rich implementation if available
- Fall back to a minimal, safe implementation otherwise
"""

from __future__ import annotations

from typing import Any, Iterable

# Try to delegate to pip's vendored rich.pretty if it exists
try:  # pragma: no cover - best-effort optional dependency
    from pip._vendor.rich.pretty import (  # type: ignore[import]
        Pretty as _RealPretty,
        pretty_repr as _real_pretty_repr,
    )

    Pretty = _RealPretty  # type: ignore[assignment]

    def pretty_repr(
        obj: Any,
        *,
        max_width: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        expand_all: bool = False,
    ) -> str:
        """
        Thin wrapper over pip._vendor.rich.pretty.pretty_repr, if available.
        """
        return _real_pretty_repr(
            obj,
            max_width=max_width,
            max_string=max_string,
            max_depth=max_depth,
            expand_all=expand_all,
        )

except Exception:
    # Fallback: very small, test-safe Pretty implementation

    from .text import Text  # type: ignore[import]

    class Pretty:
        """
        Minimal Pretty wrapper used when pip._vendor.rich.pretty
        is not available.

        It implements the Rich protocol enough for `Console.print`
        and for scripts._inspect to import and use it without error.
        """

        def __init__(
            self,
            obj: Any,
            *,
            expand_all: bool = False,
            max_depth: int | None = None,
            max_string: int | None = None,
            **_: Any,
        ) -> None:
            self._obj = obj
            self._expand_all = expand_all
            self._max_depth = max_depth
            self._max_string = max_string

        def __repr__(self) -> str:  # pragma: no cover - trivial
            return f"Pretty({self._obj!r})"

        def __rich_console__(self, console, options) -> Iterable["Text"]:
            """
            Very simple Rich protocol implementation: render repr(obj)
            as a plain Text.
            """
            text = Text(repr(self._obj))
            # Yield Segments via Text's __rich_console__
            yield from text.__rich_console__(console, options)

    def pretty_repr(
        obj: Any,
        *,
        max_width: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        expand_all: bool = False,
    ) -> str:
        """
        Fallback pretty_repr: just return built-in repr(obj).
        Parameters are accepted for API compatibility but ignored.
        """
        return repr(obj)


__all__ = ["Pretty", "pretty_repr"]
