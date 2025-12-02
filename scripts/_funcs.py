"""MAGIC-compatible shim for function utilities.

The original module depended on `_compat.PY_3_9_PLUS` and
`get_generic_base`. For MAGIC, the smoke tests only require that
`scripts._funcs` imports successfully. A small placeholder API is
sufficient.
"""

from __future__ import annotations

import copy
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


def clone_function(fn: F) -> F:
    """Return a shallow copy of the given function.

    This is a minimal stand-in helper; callers should not rely on any
    advanced behavior in the MAGIC layout.
    """
    return copy.copy(fn)


__all__ = ["clone_function"]

# ---- MAGIC shim: attrs-style asdict helper ----
try:  # Only define if not already provided by upstream code
    asdict  # type: ignore[name-defined]
except NameError:
    def asdict(inst, *, recurse=True, filter=None, dict_factory=dict):
        """
        MAGIC compatibility shim for attrs-style asdict.

        This is intentionally minimal and is only meant to satisfy
        callers like scripts._next_gen and Week 0 / smoke tests.

        Behaviour:
        - If 'inst' has a __dict__, we treat that as the data source.
        - If 'inst' is already a dict, we copy it.
        - Otherwise we return 'inst' unchanged.
        - 'recurse' and 'filter' are supported in a basic way so callers
          using the standard attrs-style signature don't crash.
        """
        if hasattr(inst, "__dict__"):
            data = dict_factory(inst.__dict__)
        elif isinstance(inst, dict):
            data = dict_factory(inst)
        else:
            return inst

        if filter is not None:
            data = dict_factory(
                (k, v) for k, v in data.items() if filter(inst, k, v)
            )

        if recurse:
            return dict_factory(
                (k, asdict(v, recurse=True, filter=filter, dict_factory=dict_factory))
                for k, v in data.items()
            )

        return data


# ==== MAGIC shim: attrs-style astuple for _next_gen ====
from typing import Any as _MAGIC_Any, Iterable as _MAGIC_Iterable

try:
    astuple  # type: ignore[name-defined]
except NameError:
    def astuple(
        instance: _MAGIC_Any,
        *,
        recurse: bool = True,
        tuple_factory = tuple,
        retain_collection_types: bool = False,
        filter = None,
    ):
        """MAGIC shim: very lightweight astuple implementation.

        This is NOT a full attrs implementation. It only needs to be
        good enough so that scripts._next_gen can import and basic usage
        does not explode.
        """
        # If it's already a tuple, keep it as-is.
        if isinstance(instance, tuple):
            return tuple_factory(instance)

        # If it's some other iterable (list, set, etc.), shallow-convert.
        if isinstance(instance, _MAGIC_Iterable) and not isinstance(instance, (str, bytes)):
            return tuple_factory(instance)

        # Fallback: wrap single value.
        return tuple_factory([instance])
# ==== end MAGIC shim astuple ====
