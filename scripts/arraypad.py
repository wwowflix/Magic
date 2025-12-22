"""
MAGIC stub: lightweight arraypad replacement for smoke tests.

The real numpy.lib.arraypad module provides many padding modes and helpers.
For MAGIC we only need a small, safe wrapper around numpy.pad so that the
module imports cleanly and basic padding can be exercised in tests.
"""

from typing import Any, Iterable, Sequence, Tuple, Union

import numpy as np

PadWidth = Union[int, Sequence[Tuple[int, int]], Sequence[int]]


def pad(
    array: Any,
    pad_width: PadWidth,
    mode: str = "constant",
    constant_values: Any = 0,
) -> np.ndarray:
    """
    Thin wrapper around numpy.pad with a simplified signature.

    Parameters
    ----------
    array : Any
        Input array-like object.
    pad_width : int or sequence
        Number of values padded to the edges of each axis.
    mode : str, default "constant"
        Padding mode passed to numpy.pad.
    constant_values : Any, default 0
        Constant value for "constant" mode.
    """
    arr = np.asarray(array)
    return np.pad(arr, pad_width, mode=mode, constant_values=constant_values)
