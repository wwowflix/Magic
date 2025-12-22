from __future__ import annotations

"""
MAGIC stub: lightweight replacement for pandas.core.dtypes.astype

The real pandas "astype" module has a lot of logic for dtype conversions,
NaN handling, datetime/timedelta casting, etc.

For MAGIC we only need:
- imports to succeed
- a couple of simple helpers that behave like "astype" for basic arrays
  without depending on internal pandas dtypes such as PandasDtype.
"""

from typing import Any

import numpy as np


def astype_array(
    values: Any,
    dtype: Any,
    copy: bool = True,
    errors: str = "raise",
) -> np.ndarray:
    """
    Very small stand-in for pandas' astype_array.

    * Wraps values with numpy.asarray and applies dtype.
    * If errors="ignore" and casting fails, returns the original values.
    * For errors="raise", the original exception is propagated.
    """
    arr = np.asarray(values)
    try:
        result = arr.astype(dtype, copy=copy)
    except (TypeError, ValueError):
        if errors == "ignore":
            # Behave like pandas: return original values unchanged
            return arr
        raise
    return result


def astype_nansafe(values: Any, dtype: Any, copy: bool = True) -> np.ndarray:
    """
    Simplified version of pandas.core.dtypes.astype.astype_nansafe.

    It does NOT implement full NaN / datetime / timedelta rules, but it
    gives a predictable, safe conversion for basic numeric/object arrays.
    """
    arr = np.asarray(values)
    # For the stub, delegate to numpy.astype; callers in MAGIC tests only
    # care that the function exists and works on simple inputs.
    return arr.astype(dtype, copy=copy)


def convert_dtype(values: Any, dtype: Any) -> np.ndarray:
    """
    Tiny convenience wrapper used in some call sites.

    This is *not* the real pandas 'convert_dtypes', just a helper that
    calls astype_array with default settings.
    """
    return astype_array(values, dtype)
