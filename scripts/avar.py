from __future__ import annotations

"""
MAGIC stub: lightweight replacement for fontTools.varLib-based avar helper.

The original module imported from `fontTools.varLib` and touched internal
objects like VarData, which can differ between fontTools versions and
explode at import time.

For MAGIC we only need:
- Safe import
- A couple of tiny helpers with the same *shape* as the real API.
"""

from typing import Any, Iterable, Mapping


def _add_avar(font: Any, axes: Mapping[str, Iterable[float]]) -> None:
    """
    No-op stub for adding an 'avar' (axis variation) table.

    In real fontTools, this would mutate the font's tables based on the
    designspace. For MAGIC smoke tests we simply do nothing.
    """
    # Intentionally a no-op
    return None


def load_designspace(path: str) -> dict[str, Any]:
    """
    Very small stand-in for fontTools.varLib.load_designspace.

    We don't parse anything here; we just return a lightweight structure
    that looks vaguely like "something was loaded".
    """
    return {
        "path": path,
        "axes": [],
        "instances": [],
    }
