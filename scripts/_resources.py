"""MAGIC shim for trio._resources-like module."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from types import TracebackType
from typing import Optional, Type


class AsyncResource(metaclass=ABCMeta):
    """Minimal asynchronous resource interface used in MAGIC tests."""

    @abstractmethod
    async def aclose(self) -> None:  # pragma: no cover - trivial shim
        """Close the resource."""

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()
