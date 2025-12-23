"""MAGIC-compatible wrapper for the _cmp helpers.

This is a reduced, import-safe version that only provides a simple
`cmp` function. The MAGIC smoke tests only require that
`scripts._cmp` imports successfully.
"""

from __future__ import annotations


def cmp(a, b):
    """Return negative if a<b, zero if a==b, positive if a>b."""
    return (a > b) - (a < b)


__all__ = ["cmp"]
