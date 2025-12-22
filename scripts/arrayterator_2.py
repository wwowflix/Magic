from typing import Any, TYPE_CHECKING
import numpy as np

AR_i8: np.ndarray[Any, np.dtype[np.int64]]


def make_iterator(x: Any) -> np.lib.Arrayterator:
    """
    Small helper used so tests can import and call something from
    this module if needed. Wraps numpy.lib.Arrayterator.
    """
    arr = np.asarray(x)
    return np.lib.Arrayterator(arr)


if TYPE_CHECKING:
    # This is only for static type checkers; it will never run at runtime,
    # so it cannot raise NameError during imports.
    ar_iter = np.lib.Arrayterator(AR_i8)
