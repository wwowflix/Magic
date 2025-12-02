from __future__ import annotations

"""
MAGIC stub: lightweight async filesystem helpers for smoke tests.

The original module (from fsspec) exposes high-level async file-system
utilities and depends on implementations.local and custom exceptions.

For MAGIC we only need:
- the module to import cleanly, and
- a tiny AsyncFileSystem + AsyncFile that can be used in simple tests.
"""

import asyncio
from typing import Any, Awaitable


class AsyncFile:
    """
    Very small in-memory async file object.

    It supports async context-manager protocol and read/write methods,
    which is enough for our smoke tests.
    """

    def __init__(self, path: str, mode: str = "rb") -> None:
        self.path = path
        self.mode = mode
        self._buffer: bytearray = bytearray()

    async def __aenter__(self) -> "AsyncFile":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # pragma: no cover
        return None

    async def read(self) -> bytes:
        return bytes(self._buffer)

    async def write(self, data: Any) -> int:
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif not isinstance(data, (bytes, bytearray)):
            data = str(data).encode("utf-8")
        self._buffer.extend(data)
        return len(data)


class AsyncFileSystem:
    """
    Minimal async file-system facade.

    Real fsspec AsyncFileSystem is much more powerful; here we just
    provide an async `open()` method returning an AsyncFile instance.
    """

    async def open(
        self,
        path: str,
        mode: str = "rb",
        *args: Any,
        **kwargs: Any,
    ) -> AsyncFile:
        return AsyncFile(path, mode=mode)


async def _sleep(delay: float = 0.0) -> None:
    """
    Tiny helper to exercise an async API in tests.
    """
    await asyncio.sleep(delay)


def run(coro: Awaitable[Any]) -> Any:
    """
    Run a coroutine to completion; small utility for tests that do not
    manage their own event loop.
    """
    return asyncio.run(coro)
