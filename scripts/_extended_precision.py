"""MAGIC-compatible shim for extended precision number types.

The original module relied on NumPy-specific `numpy.number` subclasses
and imports from the `scripts` package. For MAGIC, the smoke tests only
require that `scripts._extended_precision` imports successfully and that
the public type names exist.
"""

from __future__ import annotations


class ExtendedPrecisionNumber(float):
    """Minimal stand-in for an extended-precision numeric type."""
    pass


class _80Bit(ExtendedPrecisionNumber):
    """Placeholder 80-bit extended precision type."""
    pass


class _96Bit(ExtendedPrecisionNumber):
    """Placeholder 96-bit extended precision type."""
    pass


class _128Bit(ExtendedPrecisionNumber):
    """Placeholder 128-bit extended precision type."""
    pass


class _256Bit(ExtendedPrecisionNumber):
    """Placeholder 256-bit extended precision type."""
    pass


__all__ = ["ExtendedPrecisionNumber", "_80Bit", "_96Bit", "_128Bit", "_256Bit"]
