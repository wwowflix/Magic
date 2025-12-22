"""MAGIC shim for trio._tasks-like helpers."""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager


class CancelScope(AbstractAsyncContextManager):
    """Tiny stand-in for trio.CancelScope."""

    def __init__(self) -> None:
        self.cancel_called = False

    def cancel(self) -> None:
        self.cancel_called = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False
