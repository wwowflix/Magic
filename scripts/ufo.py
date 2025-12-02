from __future__ import annotations

"""
Week 0 stub for scripts.ufo.

The real module converts cubic curves to quadratic splines and depends
on other fontTools helpers like curves_to_quadratic. For smoke-import
tests we only need the public functions that CLI code imports:

- ont_to_quadratic
- onts_to_quadratic

These stubs provide import-safe no-op implementations.
"""

from typing import Any, Iterable, Tuple


def font_to_quadratic(font: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Stubbed converter for a single font.

    For Week 0 this simply returns the input font unchanged.
    """
    return font


def fonts_to_quadratic(fonts: Iterable[Any], *args: Any, **kwargs: Any) -> Tuple[list[Any], dict]:
    """
    Stubbed converter for multiple fonts.

    For Week 0 this returns a list copy of the input fonts and an empty
    metadata dict.
    """
    return list(fonts), {}
