from __future__ import annotations

"""
MAGIC shim for scripts.array_2

Original module was a vendored pandas SparseArray implementation that
relied on internal pandas APIs like
`pandas.core.dtypes.astype.astype_nansafe`, which are not available in
this environment.

For MAGIC smoke tests we only need:

- `import scripts.array_2` to succeed.
- A small, predictable SparseArray-like object for any light usage.

This shim provides:

- SparseArray: a minimal wrapper around a Python sequence (or NumPy
  array) with a few basic helpers.
"""

from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class SparseArray:
    """
    Minimal stand-in for a sparse array.

    This is NOT a full pandas SparseArray; it just stores the data as a
    plain Python list and exposes a few convenience methods.
    """

    data: List[Any]

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is None:
            self.data = []
        else:
            self.data = list(data)

    def to_dense(self) -> list[Any]:
        """Return the underlying data as a dense list."""
        return list(self.data)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self.data)

    def __iter__(self):  # pragma: no cover - trivial
        return iter(self.data)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"SparseArray({self.data!r})"


__all__ = ["SparseArray"]
