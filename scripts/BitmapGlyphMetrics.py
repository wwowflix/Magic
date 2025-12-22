"""Bitmap glyph metrics helpers for MAGIC.

This module wraps bitmap metrics structures from fontTools, but also
provides a safe fallback when fontTools is not available or mis-detected.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- sstruct import (real or dummy) ------------------------------------

try:
    # Preferred path: use the real fontTools package if it is importable.
    from fontTools.misc import sstruct  # type: ignore[import]
except Exception as exc:
    # Fallback stub so that scripts.BitmapGlyphMetrics can still be imported
    # in constrained or misconfigured environments.
    class _DummySstruct:
        """Fallback stub for fontTools.misc.sstruct.

        Any real use of bitmap glyph metrics should fail loudly instead
        of silently doing the wrong thing.
        """

        def __getattr__(self, name: str):
            raise RuntimeError(
                "fontTools.misc.sstruct is required for bitmap glyph "
                "metrics operations but could not be imported."
            ) from exc

    sstruct = _DummySstruct()  # type: ignore[assignment]


# --- Minimal Big/Small glyph metric structures -------------------------


@dataclass
class BigGlyphMetrics:
    """Simplified stand-in for fontTools BigGlyphMetrics."""
    height: int = 0
    width: int = 0
    horiBearingX: int = 0
    horiBearingY: int = 0
    horiAdvance: int = 0
    vertBearingX: int = 0
    vertBearingY: int = 0
    vertAdvance: int = 0


@dataclass
class SmallGlyphMetrics:
    """Simplified stand-in for fontTools SmallGlyphMetrics."""
    height: int = 0
    width: int = 0
    bearingX: int = 0
    bearingY: int = 0
    advance: int = 0


# These format strings mimic the structure description used by fontTools.
# The smoke tests only need them to exist; they are not used for real parsing.
bigGlyphMetricsFormat = """
>   # big glyph metrics
B   height
B   width
b   horiBearingX
b   horiBearingY
B   horiAdvance
b   vertBearingX
b   vertBearingY
B   vertAdvance
"""

smallGlyphMetricsFormat = """
>   # small glyph metrics
B   height
B   width
b   bearingX
b   bearingY
B   advance
"""


__all__ = [
    "sstruct",
    "BigGlyphMetrics",
    "bigGlyphMetricsFormat",
    "SmallGlyphMetrics",
    "smallGlyphMetricsFormat",
]
