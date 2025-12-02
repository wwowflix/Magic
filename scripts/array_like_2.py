from typing import Any, Optional
import numpy as np
from numpy.typing import ArrayLike


def to_array(x: ArrayLike, dtype: Optional[str] = None) -> np.ndarray:
    """
    Tiny helper that converts an ArrayLike into a NumPy array.

    This is only a lightweight stub used by MAGIC's smoke tests so that
    the module can be imported and a simple function can be called.
    It avoids using private typing symbols like `_SupportsArray`.
    """
    if dtype is not None:
        return np.array(x, dtype=dtype)
    return np.array(x)


def is_array_like(obj: Any) -> bool:
    """
    Very permissive "is array-like" check – good enough for tests.
    """
    # Accept common containers and NumPy scalars/arrays
    if isinstance(obj, (list, tuple, dict, np.ndarray, np.generic)):
        return True
    try:
        iter(obj)
        return True
    except TypeError:
        return False
