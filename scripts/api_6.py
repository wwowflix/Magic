"""
MAGIC shim: pandas index / join helpers placeholder for api_6.

The original vendored module depended on pandas.core.indexes.numeric and
other version-specific internals. For MAGIC, we only need import-time
compatibility and very small, predictable behaviour.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional, Sequence, Tuple


class Index(list):
    """Minimal Index stand-in (just a list subclass)."""

    def __repr__(self) -> str:  # pragma: no cover
        return f"Index({list(self)!r})"


class Float64Index(Index):
    pass


class Int64Index(Index):
    pass


class UInt64Index(Index):
    pass


class NumericIndex(Index):
    pass


class MultiIndex(Index):
    """Very small MultiIndex placeholder."""

    @classmethod
    def from_product(cls, iterables: Sequence[Iterable[Any]]) -> "MultiIndex":
        out: List[Tuple[Any, ...]] = []

        def _build(prefix: List[Any], rest: Sequence[Iterable[Any]]) -> None:
            if not rest:
                out.append(tuple(prefix))
                return
            head, *tail = rest
            for v in head:
                _build(prefix + [v], tail)

        _build([], list(iterables))
        return cls(out)


class DatetimeIndex(Index):
    pass


class CategoricalIndex(Index):
    pass


class IntervalIndex(Index):
    pass


def ensure_index(obj: Any) -> Index:
    """Return obj as an Index instance."""
    if isinstance(obj, Index):
        return obj
    if isinstance(obj, (list, tuple)):
        return Index(obj)
    return Index([obj])


def ensure_index_from_sequences(seqs: Sequence[Sequence[Any]]) -> Index:
    """
    Build an Index from a sequence of sequences.

    This is a very small stand-in used only for compatibility.
    """
    if not seqs:
        return Index()
    # zip(*seqs) to pair items positionally
    return Index(list(zip(*seqs)))


def _new_Index(data: Sequence[Any]) -> Index:
    """Factory used by some pandas code paths – here just wraps Index."""
    return Index(list(data))


def get_unanimous_names(indexes: Sequence[Index]) -> Optional[List[Any]]:
    """
    Placeholder for pandas.get_unanimous_names.

    We keep semantics extremely simple; returning None is safe for
    callers that only check for a unanimous name.
    """
    if not indexes:
        return None
    return None


def safe_sort(values: Sequence[Any]) -> List[Any]:
    """
    Best-effort safe sort.

    If values are not mutually comparable, we fall back to the original order.
    """
    try:
        return sorted(values)
    except Exception:
        return list(values)


__all__ = [
    "Index",
    "Float64Index",
    "Int64Index",
    "UInt64Index",
    "NumericIndex",
    "MultiIndex",
    "DatetimeIndex",
    "CategoricalIndex",
    "IntervalIndex",
    "ensure_index",
    "ensure_index_from_sequences",
    "_new_Index",
    "get_unanimous_names",
    "safe_sort",
]
