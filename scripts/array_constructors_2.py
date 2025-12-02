"""Simple array constructors shim for MAGIC smoke tests."""

from typing import Any, Iterable, Sequence, Union, overload, List

ArrayLike = Union[Sequence[Any], List[Any]]


@overload
def to_array_like(obj: ArrayLike) -> ArrayLike: ...
@overload
def to_array_like(obj: Any) -> ArrayLike: ...


def to_array_like(obj: Any) -> ArrayLike:
    """
    Very small, safe shim that converts common inputs to list-like structures.

    This is only used so that tests can import and call it without pulling in
    heavy numpy / pandas machinery.
    """
    if obj is None:
        return []
    if isinstance(obj, (list, tuple)):
        return list(obj)
    return [obj]
