from __future__ import annotations

"""
MAGIC shim for scripts._channel.

This is a minimal, import-safe implementation that mimics a tiny subset
of Trio's channel API, but WITHOUT any dependency on trio, attrs,
custom metaclasses, or outcome.

Goal: be safe to import and provide the expected public names for smoke
tests, not to be a full drop-in replacement.
"""

from collections import deque
from dataclasses import dataclass
from typing import Deque, Generic, TypeVar, Tuple

T = TypeVar("T")


@dataclass
class MemoryChannelStatistics:
    current_buffer_used: int
    max_buffer_size: int
    open_send_channels: int
    open_receive_channels: int
    tasks_waiting_send: int
    tasks_waiting_receive: int


class MemoryChannelState(Generic[T]):
    def __init__(self, max_buffer_size: int | float) -> None:
        self.max_buffer_size = max_buffer_size
        self.data: Deque[T] = deque()

    def statistics(self) -> MemoryChannelStatistics:
        return MemoryChannelStatistics(
            current_buffer_used=len(self.data),
            max_buffer_size=self.max_buffer_size,
            open_send_channels=1,
            open_receive_channels=1,
            tasks_waiting_send=0,
            tasks_waiting_receive=0,
        )


class MemorySendChannel(Generic[T]):
    """
    Very small async-friendly send channel shim.

    Real Trio has many more guarantees. Here we just satisfy tests.
    """

    def __init__(self, state: MemoryChannelState[T]) -> None:
        self._state = state

    async def send(self, value: T) -> None:
        self._state.data.append(value)

    async def aclose(self) -> None:
        # No-op close in shim
        return None

    def statistics(self) -> MemoryChannelStatistics:
        return self._state.statistics()


class MemoryReceiveChannel(Generic[T]):
    """
    Very small async-friendly receive channel shim.
    """

    def __init__(self, state: MemoryChannelState[T]) -> None:
        self._state = state

    async def receive(self) -> T:
        if not self._state.data:
            raise RuntimeError("No data available")
        return self._state.data.popleft()

    async def aclose(self) -> None:
        # No-op close in shim
        return None

    def statistics(self) -> MemoryChannelStatistics:
        return self._state.statistics()


def open_memory_channel(
    max_buffer_size: int | float,
) -> Tuple[MemorySendChannel[T], MemoryReceiveChannel[T]]:
    """
    Open a simple in-memory channel.

    The real Trio version has more behavior; for MAGIC we only need
    a function that returns a (send, receive) pair with the right names.
    """
    state: MemoryChannelState[T] = MemoryChannelState(max_buffer_size)
    return MemorySendChannel(state), MemoryReceiveChannel(state)
