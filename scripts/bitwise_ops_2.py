from __future__ import annotations

"""
MAGIC stub: second variant of bitwise operations.

We provide a left-shift helper that is safe on integer arrays.
"""

from typing import Any
import numpy as np


def safe_left_shift(values: Any, shift: int) -> np.ndarray:
    arr = np.asarray(values, dtype="int64")
    return arr << int(shift)
