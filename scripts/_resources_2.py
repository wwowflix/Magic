"""MAGIC shim for secondary resource helpers."""
from __future__ import annotations

from ._tasks import CancelScope  # type: ignore[import]

__all__ = ["CancelScope"]
