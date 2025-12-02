"""MAGIC-compatible placeholder for dtype utilities.

This is a minimal, import-safe shim. The MAGIC smoke tests only require
that `scripts._dtype` can be imported; full dtype behavior is not needed.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class DType:
    """Very small stand-in type object."""
    name: str = "generic"


def as_dtype(obj: Any) -> DType:
    """Best-effort conversion to a DType placeholder."""
    if isinstance(obj, DType):
        return obj
    return DType(name=str(getattr(obj, "name", obj)))


__all__ = ["DType", "as_dtype"]
