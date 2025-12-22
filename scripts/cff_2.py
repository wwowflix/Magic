from __future__ import annotations

"""
MAGIC stub: safe placeholder for a second CFF helper module (cff_2).

Original version tried to import `fontTools.varLib` and triggered the
VarData/VarRegion machinery. For MAGIC Week 0 we only need:

- `import scripts.cff_2` to succeed
- A tiny, harmless API surface that looks "font-related"
"""

from typing import Any, Iterable

try:
    # Prefer to reuse the primary CFF stub if available
    from .cff import subset_cff as _subset_cff, CFFSubsetter as _CFFSubsetter
except Exception:  # pragma: no cover
    _subset_cff = None
    _CFFSubsetter = None


class CFF2Subsetter:
    """
    Minimal stand-in for a second-stage CFF subsetter.

    In a real implementation this might build on varLib logic.
    Here we just keep a reference to the font object.
    """

    def __init__(self, font: Any) -> None:  # pragma: no cover
        self.font = font

    def subset(self, glyphs: Iterable[str] | None = None) -> None:  # pragma: no cover
        # No-op; Week 0 does not mutate fonts.
        return None


def subset_cff2(font: Any, glyphs: Iterable[str] | None = None) -> Any:
    """
    Convenience helper mirroring a typical "subset CFF v2" API.

    For Week 0:
    - Optionally call the base `subset_cff` if it exists
    - Always return the original font unchanged
    """
    if _subset_cff is not None:
        _subset_cff(font, glyphs)
    _ = CFF2Subsetter(font)
    return font
