"""
MAGIC shim: pandas dtypes common helpers placeholder.

This replaces a pandas-version-sensitive module with a lightweight,
import-safe set of helpers. Functions here are intentionally simple
and conservative – they mostly serve as capability flags and basic
type checks, not full pandas semantics.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _always_false(*args: Any, **kwargs: Any) -> bool:
    return False


def _always_true(*args: Any, **kwargs: Any) -> bool:
    return True


def _identity(x: Any, *args: Any, **kwargs: Any) -> Any:
    return x


# ---- Basic helpers --------------------------------------------------------


def is_array_like(obj: Any) -> bool:
    # Treat non-string iterables as array-like.
    if isinstance(obj, (str, bytes)):
        return False
    return isinstance(obj, Iterable)


def is_bool(obj: Any) -> bool:
    return isinstance(obj, bool)


def is_bool_dtype(obj: Any) -> bool:
    # Very small stand-in: True for bool type itself or bool instances.
    return obj is bool or isinstance(obj, bool)


def is_float(obj: Any) -> bool:
    return isinstance(obj, float)


def is_float_dtype(obj: Any) -> bool:
    return obj is float


def is_integer(obj: Any) -> bool:
    return isinstance(obj, int) and not isinstance(obj, bool)


def is_integer_dtype(obj: Any) -> bool:
    return obj is int


def is_list_like(obj: Any) -> bool:
    return is_array_like(obj)


def is_dict_like(obj: Any) -> bool:
    return isinstance(obj, dict)


def is_scalar(obj: Any) -> bool:
    # Scalar if not array-like and not dict-like.
    return not is_array_like(obj) and not is_dict_like(obj)


def is_hashable(obj: Any) -> bool:
    try:
        hash(obj)
    except TypeError:
        return False
    return True


def is_iterator(obj: Any) -> bool:
    return hasattr(obj, "__iter__") and hasattr(obj, "__next__")


def is_number(obj: Any) -> bool:
    return isinstance(obj, (int, float)) and not isinstance(obj, bool)


def is_numeric_dtype(obj: Any) -> bool:
    return obj in (int, float)


def is_string_dtype(obj: Any) -> bool:
    return obj in (str, bytes)


def is_object_dtype(obj: Any) -> bool:
    # Minimal: treat anything else as "object-like".
    return not is_numeric_dtype(obj) and not is_string_dtype(obj)


# ---- Stubs for pandas-specific concepts ----------------------------------
# These are kept very simple and mostly return False; they exist only so code
# can safely call them or check for their presence.


def is_categorical(*args: Any, **kwargs: Any) -> bool:
    return False


def is_categorical_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_complex(*args: Any, **kwargs: Any) -> bool:
    return False


def is_complex_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_datetime64_any_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_datetime64_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_datetime64_ns_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_datetime64tz_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_dtype_equal(*args: Any, **kwargs: Any) -> bool:
    # Very small placeholder: equality by == if possible.
    if not args:
        return False
    first = args[0]
    return all(a == first for a in args[1:])


def is_extension_array_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_extension_type(*args: Any, **kwargs: Any) -> bool:
    return False


def is_file_like(obj: Any) -> bool:
    return hasattr(obj, "read") or hasattr(obj, "write")


def is_int64_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_interval(*args: Any, **kwargs: Any) -> bool:
    return False


def is_interval_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_named_tuple(obj: Any) -> bool:
    return isinstance(obj, tuple) and hasattr(obj, "_fields")


def is_period_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_re(obj: Any) -> bool:
    # Regex objects in Python typically have "search" or "match" attributes.
    return hasattr(obj, "search") or hasattr(obj, "match")


def is_re_compilable(obj: Any) -> bool:
    # Very permissive: assume strings are compilable.
    return isinstance(obj, (str, bytes))


def is_signed_integer_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_sparse(*args: Any, **kwargs: Any) -> bool:
    return False


def is_timedelta64_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_timedelta64_ns_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def is_unsigned_integer_dtype(*args: Any, **kwargs: Any) -> bool:
    return False


def pandas_dtype(obj: Any, *args: Any, **kwargs: Any) -> Any:
    """Identity placeholder for pandas_dtype coercion."""
    return _identity(obj, *args, **kwargs)


__all__ = [
    "is_array_like",
    "is_bool",
    "is_bool_dtype",
    "is_categorical",
    "is_categorical_dtype",
    "is_complex",
    "is_complex_dtype",
    "is_datetime64_any_dtype",
    "is_datetime64_dtype",
    "is_datetime64_ns_dtype",
    "is_datetime64tz_dtype",
    "is_dict_like",
    "is_dtype_equal",
    "is_extension_array_dtype",
    "is_extension_type",
    "is_file_like",
    "is_float",
    "is_float_dtype",
    "is_hashable",
    "is_int64_dtype",
    "is_integer",
    "is_integer_dtype",
    "is_interval",
    "is_interval_dtype",
    "is_iterator",
    "is_list_like",
    "is_named_tuple",
    "is_number",
    "is_numeric_dtype",
    "is_object_dtype",
    "is_period_dtype",
    "is_re",
    "is_re_compilable",
    "is_scalar",
    "is_signed_integer_dtype",
    "is_sparse",
    "is_string_dtype",
    "is_timedelta64_dtype",
    "is_timedelta64_ns_dtype",
    "is_unsigned_integer_dtype",
    "pandas_dtype",
]
