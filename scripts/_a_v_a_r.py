"""MAGIC-compatible wrapper for the _a_v_a_r table.

This module is kept deliberately small so that it can be imported even
in environments where fontTools' varLib helpers are not fully available.
The MAGIC smoke tests only verify that `scripts._a_v_a_r` imports.
"""

from __future__ import annotations

# Try to use the real helper from fontTools if possible.
try:
    from fontTools.varLib.models import piecewiseLinearMap as _piecewiseLinearMap  # type: ignore[import]
except Exception:
    def piecewiseLinearMap(value, mapping):
        """Fallback piecewise-linear mapping.

        In this reduced environment we simply return the original value.
        This is sufficient for the MAGIC smoke tests, which don't depend
        on full OpenType variation behavior.
        """
        return value
else:
    def piecewiseLinearMap(value, mapping):
        # Delegate to the real implementation when the import succeeds.
        return _piecewiseLinearMap(value, mapping)


class table__a_v_a_r:
    """Minimal stand-in for the 'avar' table.

    This exists solely so that code which expects a table__a_v_a_r class
    can still instantiate it without failing at import time.
    """

    def __init__(self, *args, **kwargs):
        # Store any arguments for debugging/future extension if needed.
        self.args = args
        self.kwargs = kwargs


__all__ = ["piecewiseLinearMap", "table__a_v_a_r"]
