"""
MAGIC Week 0 shim for dim2.

Original vendored version depended on internal pandas details like
`pandas.core.arrays.integer.INT_STR_TO_DTYPE`, which are not stable
across versions.

For MAGIC Week 0 smoke tests we only need:
- this module to import successfully
- a tiny, self-contained API that won’t touch pandas internals
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


# Very small stand-in mapping for integer dtype names.
INT_STR_TO_DTYPE: Dict[str, str] = {
    "int8": "int8",
    "int16": "int16",
    "int32": "int32",
    "int64": "int64",
    "uint8": "uint8",
    "uint16": "uint16",
    "uint32": "uint32",
    "uint64": "uint64",
}


@dataclass
class Dim2Summary:
    """
    Tiny placeholder for whatever "2D dimension" logic the original
    example might have had.

    Week 0: we only store shape as (rows, cols) and echo it back.
    """

    rows: int
    cols: int

    @property
    def shape(self) -> tuple[int, int]:
        return (self.rows, self.cols)


def summarize_2d(values: Iterable[Iterable[Any]]) -> Dim2Summary:
    """
    Compute a very small summary over a 2-D iterable.

    This is only here so the module has at least one trivial function
    for debugging and future extension.  It is NOT used by smoke tests.
    """
    rows_list: List[List[Any]] = [list(row) for row in values]
    rows = len(rows_list)
    cols = len(rows_list[0]) if rows_list else 0
    return Dim2Summary(rows=rows, cols=cols)
