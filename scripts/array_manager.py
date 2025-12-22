from __future__ import annotations

"""
MAGIC stub: lightweight ArrayManager replacement for smoke tests.

This avoids importing heavy pandas internals like
pandas.core.dtypes.cast.soft_convert_objects, but still provides a small
class with a couple of basic methods so tests can import and do light usage.
"""

from typing import Any, Iterable, List, Sequence

import numpy as np


class ArrayManager:
    """
    Extremely small stand-in for pandas' ArrayManager.

    It stores a list of 1D numpy arrays and simple "axes" metadata.
    """

    def __init__(
        self,
        arrays: Sequence[np.ndarray] | None = None,
        axes: Sequence[Any] | None = None,
    ) -> None:
        self.arrays: List[np.ndarray] = list(arrays) if arrays is not None else []
        self.axes: List[Any] = list(axes) if axes is not None else []

    def __len__(self) -> int:
        return len(self.arrays)

    def copy(self) -> "ArrayManager":
        """Return a shallow copy of this ArrayManager."""
        return ArrayManager(
            arrays=[arr.copy() for arr in self.arrays],
            axes=list(self.axes),
        )

    def to_numpy(self) -> np.ndarray:
        """
        Convert to a 2D numpy array (columns = stored arrays).
        """
        if not self.arrays:
            return np.empty((0, 0))
        return np.column_stack(self.arrays)


def create_array_manager(data: Iterable[Iterable[Any]]) -> ArrayManager:
    """
    Convenience helper used by potential tests: create an ArrayManager
    from an iterable-of-iterables.
    """
    arrays = [np.array(col) for col in data]
    axes = [np.arange(len(arrays[0]))] if arrays else []
    return ArrayManager(arrays=arrays, axes=axes)
