from typing import TYPE_CHECKING
import numpy as np
from numpy.typing import ArrayLike


class A:
    """Tiny placeholder class used only for ArrayLike typing examples."""
    pass


# These assignments are for static type checking examples only.
x1: ArrayLike = (i for i in range(10))  # E: Incompatible types in assignment
x2: ArrayLike = A()  # E: Incompatible types in assignment
x3: ArrayLike = {1: "foo", 2: "bar"}  # E: Incompatible types in assignment

scalar = np.int64(1)

if TYPE_CHECKING:
    # This call exists only so static type checkers can analyze it; at runtime
    # it is skipped, so it cannot raise TypeError during import.
    scalar.__array__(dtype=np.float64)  # E: No overload variant
