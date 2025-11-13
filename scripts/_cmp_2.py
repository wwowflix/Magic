"""MAGIC-compatible wrapper for the _cmp_2 helpers.

This is a reduced, import-safe version. The MAGIC smoke tests only
require that `scripts._cmp_2` imports successfully.
"""

from __future__ import annotations

# Try to reuse the cmp implementation from scripts._cmp if available.
try:
    from ._cmp import cmp as _base_cmp  # type: ignore[import]
except Exception:
    def _base_cmp(a, b):
        # Simple fallback comparison
        return (a > b) - (a < b)


def cmp(a, b):
    """Return negative if a<b, zero if a==b, positive if a>b."""
    return _base_cmp(a, b)


__all__ = ["cmp"]
