from __future__ import annotations

"""
MAGIC stub: safe replacement for a NumPy bitwise ops demo.

The original module executed bitwise shifts at import time on unsupported
types, causing TypeError. For MAGIC we expose a tiny, safe helper.
"""

from typing import Any
import numpy as np


def safe_right_shift(values: Any, shift: int) -> np.ndarray:
    arr = np.asarray(values, dtype="int64")
    return arr >> int(shift)
