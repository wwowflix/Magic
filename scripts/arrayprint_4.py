from typing import Any, Callable, TYPE_CHECKING

import numpy as np

AR: np.ndarray[Any, Any]
func_float: Callable[[np.floating[Any]], str]
func_int: Callable[[np.integer[Any]], str]


def format_value(x: Any) -> str:
    """
    Simple formatter used so tests can import and call something
    from this module if needed.
    """
    arr = np.asarray(x)
    return np.array2string(arr)


if TYPE_CHECKING:
    # This is only for static type checkers (e.g. mypy). It will never run
    # at runtime, so it cannot raise NameError during imports.
    reveal_type(np.get_printoptions())  # E: TypedDict
