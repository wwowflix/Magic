from __future__ import annotations

"""
Week 0 stub for `scripts.column`.

The original module integrates with pandas' dataframe interchange
protocol and imports internal helpers like `NoBufferPresent` which
may not exist in the installed pandas version.

For MAGIC Week 0, we only need this module to import cleanly and to
provide a minimal Column-like object.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Sequence


class DtypeKind(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    UNKNOWN = auto()


class ColumnNullType(Enum):
    NON_NULLABLE = auto()
    USE_NAN = auto()
    USE_SENTINEL = auto()


@dataclass
class Column:
    """
    Minimal stand-in for a column object in a dataframe.

    This is intentionally tiny: just enough for tests or other code
    that inspects attributes like `size` or indexes into the data.
    """

    data: Sequence[Any]
    name: str | None = None
    dtype_kind: DtypeKind = DtypeKind.UNKNOWN
    null_type: ColumnNullType = ColumnNullType.NON_NULLABLE

    @property
    def size(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Any:
        return self.data[idx]
