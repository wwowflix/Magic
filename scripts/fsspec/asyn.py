from __future__ import annotations

"""
MAGIC Week 0 stub for `fsspec.asyn`.

Provides:
- AbstractAsyncStreamedFile
- AsyncFileSystem
- sync
- sync_wrapper

No real async filesystem or network I/O; just minimal placeholders so
imports and basic usage do not explode.
"""

from typing import Any, Awaitable, Callable, TypeVar, Optional
import asyncio

_T = TypeVar("_T")


class AbstractAsyncStreamedFile:
    """
    Minimal stub for fsspec.asyn.AbstractAsyncStreamedFile.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed = False

    async def __aenter__(self) -> "AbstractAsyncStreamedFile":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        await self.close()
        return False

    async def read(self, *args: Any, **kwargs: Any) -> bytes:
        raise OSError("MAGIC Week 0 stub: async file read not available")

    async def close(self) -> None:
        self._closed = True


class AsyncFileSystem:
    """
    Minimal stub for fsspec.asyn.AsyncFileSystem.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed = False

    async def _open(self, *args: Any, **kwargs: Any) -> AbstractAsyncStreamedFile:
        raise OSError("MAGIC Week 0 stub: async filesystem not available")

    async def close(self) -> None:
        self._closed = True


def sync(loop: Optional[asyncio.AbstractEventLoop], awaitable: Awaitable[_T]) -> _T:
    """
    Very small stand-in for fsspec.asyn.sync.

    For Week 0, just run the awaitable in a fresh event loop if needed.
    """
    if asyncio.iscoroutine(awaitable):
        return asyncio.run(awaitable)  # type: ignore[return-value]
    return awaitable  # type: ignore[return-value]


def sync_wrapper(fn: Callable[..., Awaitable[_T]]) -> Callable[..., _T]:
    """
    Decorator converting an async function into a sync one using `sync`.
    """

    def wrapped(*args: Any, **kwargs: Any) -> _T:
        return sync(None, fn(*args, **kwargs))

    return wrapped


__all__ = [
    "AbstractAsyncStreamedFile",
    "AsyncFileSystem",
    "sync",
    "sync_wrapper",
]
