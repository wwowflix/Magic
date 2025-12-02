"""
MAGIC shim: lightweight pandas-like algorithms placeholder.

Replaces the heavy pandas.algorithms vendored code with simple,
pure-Python helpers that are safe to import in this environment.
"""

from __future__ import annotations

from typing import Any, Sequence, Tuple, List, Dict


def value_counts(values: Sequence[Any]) -> Dict[Any, int]:
    """Return a simple value -> count mapping."""
    counts: Dict[Any, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return counts


def unique(values: Sequence[Any]) -> List[Any]:
    """Return list of unique items preserving input order."""
    seen: List[Any] = []
    for v in values:
        if v not in seen:
            seen.append(v)
    return seen


def factorize(values: Sequence[Any]) -> Tuple[List[int], List[Any]]:
    """
    Simple factorize implementation.

    Returns (codes, uniques) where codes[i] is the index of values[i]
    in the uniques list.
    """
    uniques = unique(values)
    codes: List[int] = [uniques.index(v) for v in values]
    return codes, uniques


__all__ = ["value_counts", "unique", "factorize"]
