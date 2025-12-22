from __future__ import annotations

"""
MAGIC stub: lightweight replacement for pandas.testing.asserters

The real pandas.asserters module has many helpers for comparing Series,
DataFrames, Index objects, and arrays. For MAGIC we only need a small,
safe subset so that tests can import this module and call a few common
helpers without pulling in private pandas internals like PandasDtype.
"""

from typing import Any

import numpy as np

try:  # use real pandas.testing if available
    import pandas as pd
except Exception:  # pragma: no cover - very defensive
    pd = None  # type: ignore[assignment]


def assert_almost_equal(left: Any, right: Any, **kwargs: Any) -> None:
    """
    Compare two scalars/arrays for approximate equality.

    Delegates to numpy.testing.assert_allclose for arrays.
    """
    if isinstance(left, np.ndarray) or isinstance(right, np.ndarray):
        np.testing.assert_allclose(left, right, **kwargs)
    else:
        if left != right:
            raise AssertionError(f"{left!r} != {right!r}")


def assert_series_equal(left: Any, right: Any, **kwargs: Any) -> None:
    """
    Thin wrapper around pandas.testing.assert_series_equal if pandas is present.
    Falls back to simple value comparison otherwise.
    """
    if pd is not None:
        pd.testing.assert_series_equal(left, right, **kwargs)  # type: ignore[attr-defined]
    else:
        if list(left) != list(right):
            raise AssertionError("Series values differ")


def assert_frame_equal(left: Any, right: Any, **kwargs: Any) -> None:
    """
    Thin wrapper around pandas.testing.assert_frame_equal if pandas is present.
    """
    if pd is not None:
        pd.testing.assert_frame_equal(left, right, **kwargs)  # type: ignore[attr-defined]
    else:
        if getattr(left, "shape", None) != getattr(right, "shape", None):
            raise AssertionError("Frame shapes differ")
        # Very shallow check – good enough for stub
        if getattr(left, "values", None) is not None and getattr(right, "values", None) is not None:
            np.testing.assert_allclose(left.values, right.values)


def assert_index_equal(left: Any, right: Any, **kwargs: Any) -> None:
    """
    Thin wrapper around pandas.testing.assert_index_equal.
    """
    if pd is not None:
        pd.testing.assert_index_equal(left, right, **kwargs)  # type: ignore[attr-defined]
    else:
        if list(left) != list(right):
            raise AssertionError("Index values differ")


def assert_extension_array_equal(left: Any, right: Any, **kwargs: Any) -> None:
    """
    Minimal helper for ExtensionArray-like objects.

    We treat them as 1D sequences and compare with numpy.
    """
    left_arr = np.asarray(list(left))
    right_arr = np.asarray(list(right))
    np.testing.assert_array_equal(left_arr, right_arr)
