"""
MAGIC-safe shim for scripts._entry_queue.

Provides a minimal, side-effect free implementation of:

- EntryQueue: a tiny FIFO queue wrapper
- TrioToken: a lightweight token placeholder

This is enough for scripts that import these names during MAGIC smoke tests.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Generic, TypeVar

T = TypeVar("T")


@dataclass
class TrioToken:
    """Lightweight token placeholder used to tag queued items.

    The real implementation in upstream libraries carries more context,
    but for MAGIC we only need a stable, import-safe type.
    """
    id: int | None = None


class EntryQueue(Generic[T]):
    """Very small FIFO queue wrapper."""

    def __init__(self) -> None:
        self._queue: Deque[T] = deque()

    def put(self, item: T) -> None:
        """Enqueue an item."""
        self._queue.append(item)

    def get_nowait(self) -> T:
        """Dequeue an item or raise IndexError if empty."""
        if not self._queue:
            raise IndexError("EntryQueue is empty")
        return self._queue.popleft()

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._queue)


__all__ = ["EntryQueue", "TrioToken"]
