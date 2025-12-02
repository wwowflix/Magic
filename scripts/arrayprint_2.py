from typing import Callable, Any, TYPE_CHECKING

import numpy as np

# Example annotations (mainly for type checkers)
AR: np.ndarray
func1: Callable[[Any], str]
func2: Callable[[np.integer[Any]], str]


def simple_format(x: Any) -> str:
    """
    Very small helper used only so tests can import and call something
    from this module if needed.
    """
    arr = np.asarray(x)
    return np.array2string(arr)


if TYPE_CHECKING:
    # This call exists only so static type checkers can analyze it; it
    # will never execute at runtime, so it cannot raise NameError.
    np.array2string(AR, style=None)  # E: Unexpected keyword argument
