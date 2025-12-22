from __future__ import annotations

"""MAGIC Week 0 shim for scripts.pretty.

Provides:
- class Pretty
- function pretty(obj)

Goal:
- Allow safe imports by Rich-like helpers (css_types, _inspect, etc.)
- No heavy dependencies, no I/O. Real implementation will be restored in Week 1+.
"""

from typing import Any

class Pretty:
    """Very small stand-in wrapper around any object."""

    def __init__(self, obj: Any) -> None:
        self.obj = obj

    def __repr__(self) -> str:  # pragma: no cover
        return f"Pretty({self.obj!r})"


def pretty(obj: Any) -> Pretty:
    """Return a Pretty wrapper for the given object."""
    return Pretty(obj)


__all__ = ["Pretty", "pretty"]
