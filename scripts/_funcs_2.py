"""MAGIC-compatible shim for secondary function utilities.

The original module depended on `_compat.PY_3_9_PLUS` and
`get_generic_base`. For MAGIC, the smoke tests only require that
`scripts._funcs_2` imports successfully. A small placeholder API is
sufficient.
"""

from __future__ import annotations

import copy
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


def clone_function(fn: F) -> F:
    """Return a shallow copy of the given function.

    Provided for symmetry with scripts._funcs; callers should not rely
    on advanced behavior in the MAGIC layout.
    """
    return copy.copy(fn)


__all__ = ["clone_function"]
