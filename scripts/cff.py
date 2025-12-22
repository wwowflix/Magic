from __future__ import annotations

"""
MAGIC stub: safe placeholder for CFF / font subsetting helpers.

Week 0 Goal:
- `import scripts.cff` must succeed
- Avoid importing `fontTools.subset` / `fontTools.varLib`
- Provide a tiny, harmless API surface so accidental calls don’t explode
"""

from typing import Any, Iterable


class CFFSubsetter:
    """
    Minimal stand-in for a CFF subsetter.

    Real implementations would take a font and drop unused glyphs.
    Here we just store the inputs and expose a no-op subset method.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        self.args = args
        self.kwargs = kwargs

    def subset(self, glyphs: Iterable[str] | None = None) -> None:  # pragma: no cover
        # No-op: in MAGIC Week 0, we don't perform real subsetting.
        return None


def subset_cff(font: Any, glyphs: Iterable[str] | None = None) -> Any:
    """
    Convenience helper mirroring a typical "subset CFF font" API.

    For Week 0:
    - Accept a font object and an optional glyph iterable
    - Return the font unchanged
    """
    _ = CFFSubsetter(font)
    # In a real implementation we'd modify the font.
    return font
