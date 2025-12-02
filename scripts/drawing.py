from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.drawing.

Goal
----
- Let `importlib.import_module("scripts.drawing")` succeed.
- Prefer the real `fpdf.drawing` types when they exist.
- If they are missing (older / different fpdf), provide tiny stand-ins
  so that anything importing these names does not crash.

This shim is intentionally minimal and should not perform any heavy
I/O, PDF generation, or graphics work at import time.
"""

from typing import Any

try:
    # Try to use the real objects from fpdf.drawing if available.
    from fpdf.drawing import (
        ClippingPathIntersectionRule,
        IntersectionRule,
        PathPaintRule,
        StrokeCapStyle,
        StrokeJoinStyle,
        PDFStyleKeys,
    )
except Exception:  # pragma: no cover - Week 0 fallback path
    class _EnumLike(str):
        """
        Simple string-based stand-in for the real enum-like types.

        These are only meant to satisfy imports and very basic usage.
        """

        def __new__(cls, value: str) -> "_EnumLike":
            return str.__new__(cls, value)

    class ClippingPathIntersectionRule(_EnumLike):
        pass

    class IntersectionRule(_EnumLike):
        pass

    class PathPaintRule(_EnumLike):
        pass

    class StrokeCapStyle(_EnumLike):
        pass

    class StrokeJoinStyle(_EnumLike):
        pass

    # In real fpdf.drawing, PDFStyleKeys is a mapping of style names.
    # For Week 0 we just model it as a dict-like type alias.
    PDFStyleKeys = dict[str, Any]  # type: ignore[assignment]

__all__ = [
    "ClippingPathIntersectionRule",
    "IntersectionRule",
    "PathPaintRule",
    "StrokeCapStyle",
    "StrokeJoinStyle",
    "PDFStyleKeys",
]
