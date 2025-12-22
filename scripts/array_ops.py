from __future__ import annotations

"""
MAGIC stub: lightweight array_ops replacement for smoke tests.

The real pandas.array_ops module contains a large collection of functions for
arithmetic and comparison across NumPy arrays and ExtensionArrays. For MAGIC
we only need a tiny, safe subset so that imports succeed and basic operations
can be exercised without importing private pandas internals.
"""

from typing import Any

import numpy as np


def _to_array(x: Any) -> np.ndarray:
    """
    Convert common Python/NumPy inputs to a 1D numpy array.
    """
    if isinstance(x, np.ndarray):
        return x
    if isinstance(x, (list, tuple)):
        return np.asarray(x)
    return np.asarray([x])


def array_add(left: Any, right: Any) -> np.ndarray:
    """Simple elementwise addition for testing."""
    return _to_array(left) + _to_array(right)


def array_sub(left: Any, right: Any) -> np.ndarray:
    """Simple elementwise subtraction for testing."""
    return _to_array(left) - _to_array(right)


def array_mul(left: Any, right: Any) -> np.ndarray:
    """Simple elementwise multiplication for testing."""
    return _to_array(left) * _to_array(right)


def array_div(left: Any, right: Any) -> np.ndarray:
    """Simple elementwise true division for testing."""
    return _to_array(left) / _to_array(right)


def array_eq(left: Any, right: Any) -> np.ndarray:
    """Simple elementwise equality comparison."""
    return _to_array(left) == _to_array(right)
