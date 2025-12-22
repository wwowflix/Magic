from typing import List, Any, TYPE_CHECKING
import numpy as np


class SubClass(np.ndarray):
    """Minimal SubClass stub used for type and import tests only."""
    pass


i8: np.int64

A: np.ndarray
B: SubClass
C: List[int]


def func(i: int, j: int, **kwargs: Any) -> SubClass:  # type: ignore[override]
    """
    Tiny placeholder function – returns a dummy SubClass-like object.

    In real code this might construct complex numpy arrays. For MAGIC we only
    need something that can be imported and used lightly by tests.
    """
    arr = np.array([i, j], dtype="int64")
    return arr.view(SubClass)


if TYPE_CHECKING:
    # This is only for static type checkers like mypy; it will never run
    # at runtime, so it cannot cause NameError in smoke tests.
    reveal_type(np.asarray(A))  # E: numpy.ndarray[Any, Any]
