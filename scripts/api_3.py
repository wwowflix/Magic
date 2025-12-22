"""
MAGIC shim: pandas/Arrow API placeholder for import-only compatibility.

The original module depended on pandas internals like ArrowDtype that are
not available in this environment. This lightweight shim exposes a small,
stable surface area so tests can import `scripts.api_3` safely.

This is NOT a full-featured pandas implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple


# ---- NA / datetime-like placeholders -------------------------------------


class _NAType:
    """Simple singleton NA placeholder."""

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return "NA"


NA = _NAType()
NaT = None  # minimal stand-in for pandas.NaT


class Period:  # pragma: no cover - import placeholder
    """Dummy Period object used only for type compatibility."""
    pass


class Timedelta:  # pragma: no cover - import placeholder
    """Dummy Timedelta object used only for type compatibility."""
    pass


class Timestamp:  # pragma: no cover - import placeholder
    """Dummy Timestamp object used only for type compatibility."""
    pass


# ---- Categorical / ArrowDtype placeholders -------------------------------


class Categorical(list):  # pragma: no cover - trivial wrapper
    """Very small stand-in for pandas.Categorical.

    Behaves like a normal list but exists so code that expects a
    Categorical type can still run basic operations.
    """
    pass


@dataclass
class ArrowDtype:  # pragma: no cover - type placeholder
    """Minimal ArrowDtype placeholder."""

    name: str = "arrow"


# ---- Simple algorithms: factorize / unique / value_counts ----------------


def unique(values: Iterable[Any]) -> List[Any]:
    """Return list of unique items preserving input order."""
    seen: List[Any] = []
    for v in values:
        if v not in seen:
            seen.append(v)
    return seen


def value_counts(values: Iterable[Any]) -> Dict[Any, int]:
    """Return a value -> count mapping."""
    counts: Dict[Any, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return counts


def factorize(values: Iterable[Any]) -> Tuple[List[int], List[Any]]:
    """Simple factorize implementation returning (codes, uniques)."""
    uniques = unique(values)
    codes: List[int] = [uniques.index(v) for v in values]
    return codes, uniques


__all__ = [
    "NA",
    "NaT",
    "Period",
    "Timedelta",
    "Timestamp",
    "Categorical",
    "ArrowDtype",
    "unique",
    "value_counts",
    "factorize",
]
