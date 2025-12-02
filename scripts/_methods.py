from __future__ import annotations

"""
MAGIC shim for internal numerical helper methods.

Goal:
- Be safely importable as `scripts._methods`.
- Avoid heavy dependencies or complex behavior.
- If NumPy is available, lightly proxy a few helpers.
- If not, provide tiny fallbacks so callers do not crash.
"""

from typing import Any

try:  # pragma: no cover - best-effort integration
    from numpy.core import _methods as _np_methods  # type: ignore[import]
except Exception:
    _np_methods = None  # type: ignore[assignment]


def _identity(x: Any) -> Any:
    return x


# Provide a few common names that external code might expect.
# We keep them extremely lightweight – just enough for imports and basic calls.
if _np_methods is not None:
    _sum = getattr(_np_methods, "_sum", _identity)
    _prod = getattr(_np_methods, "_prod", _identity)
    _mean = getattr(_np_methods, "_mean", _identity)
else:
    _sum = _identity
    _prod = _identity
    _mean = _identity


__all__ = ["_sum", "_prod", "_mean"]
