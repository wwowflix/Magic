"""
MAGIC stub: lightweight arrayprint replacement for smoke tests.

The real numpy.core.arrayprint module contains many options and helpers for
pretty-printing arrays. For MAGIC we only need a small wrapper around
numpy.array2string so that the module imports cleanly and basic usage works.
"""

from typing import Any
import numpy as np


def array2string(
    a: Any,
    max_line_width: int | None = None,
    precision: int | None = None,
    suppress_small: bool | None = None,
    **kwargs: Any,
) -> str:
    """
    Tiny wrapper around numpy.array2string with a simplified signature.
    """
    arr = np.asarray(a)

    # We just forward kwargs we understand; others are ignored safely.
    opts: dict[str, Any] = {}
    if max_line_width is not None:
        opts["max_line_width"] = max_line_width
    if precision is not None:
        opts["precision"] = precision
    if suppress_small is not None:
        opts["suppress_small"] = suppress_small

    return np.array2string(arr, **opts)


def set_printoptions(**kwargs: Any) -> None:
    """
    Forward print options to numpy.set_printoptions for compatibility.
    """
    np.set_printoptions(**kwargs)
