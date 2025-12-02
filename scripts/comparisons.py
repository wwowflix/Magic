from __future__ import annotations

"""
Week 0 stub for `scripts.comparisons`.

The original module contains runtime comparisons that are meant as
type-checking examples, but they run at import time and cause errors.
For MAGIC Week 0, we only need safe definitions so the module imports
cleanly.
"""

from typing import Any
import numpy as np

AR_i: np.ndarray[Any, np.dtype[np.int64]] = np.array([], dtype=np.int64)
AR_f: np.ndarray[Any, np.dtype[np.float64]] = np.array([], dtype=np.float64)
AR_c: np.ndarray[Any, np.dtype[np.complex128]] = np.array([], dtype=np.complex128)
AR_m: np.ndarray[Any, np.dtype[np.timedelta64]] = np.array([], dtype="timedelta64[ns]")
AR_M: np.ndarray[Any, np.dtype[np.datetime64]] = np.array([], dtype="datetime64[ns]")


def demo() -> None:
    """No-op placeholder function for potential future tests."""
    return None
