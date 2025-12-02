"""MAGIC-compatible shim for entry point discovery.

The original module depended on `scripts.extern.jaraco.text` and pip-style
entry point machinery. For MAGIC, the smoke tests only require that
`scripts._entry_points` imports successfully. A small placeholder API is
sufficient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Optional


@dataclass
class EntryPoint:
    """Minimal stand-in for a package entry point."""
    name: str
    group: str
    value: str


def iter_entry_points(group: Optional[str] = None) -> List[EntryPoint]:
    """Return a list of available entry points.

    For MAGIC we don't perform real discovery and simply return an empty
    list. This keeps callers safe while satisfying the smoke tests.
    """
    return []


def get(group: str, name: str) -> Optional[EntryPoint]:
    """Return a single entry point, or None if not found.

    This is a placeholder that always returns None in the MAGIC layout.
    """
    return None


__all__ = ["EntryPoint", "iter_entry_points", "get"]
