from __future__ import annotations

"""
MAGIC Week 0 stub for the third-party `aiohttp` package.

Goals:
- Allow `import aiohttp` and `from aiohttp import ClientSession, ClientError, ClientConnectorError`
  to succeed for vendored scripts like scripts/http.py.
- Provide minimal async HTTP client surface (ClientSession, DummyResponse).
- NO real network I/O; everything returns dummy responses.

This is enough for imports and light attribute access during Week 0.
"""

from typing import Any, Dict, Optional


class ClientError(Exception):
    """Base error for aiohttp stub."""


class ClientConnectorError(ClientError):
    """Connection error in aiohttp stub."""


class DummyResponse:
    """Very small stand-in for aiohttp.ClientResponse."""

    def __init__(self, status: int = 200, text: str = "", content: bytes = b"") -> None:
        self.status = status
        self._text = text
        self._content = content
        self.headers: Dict[str, str] = {}

    async def text(self, *args: Any, **kwargs: Any) -> str:
        return self._text

    async def read(self, *args: Any, **kwargs: Any) -> bytes:
        return self._content

    async def json(self, *args: Any, **kwargs: Any) -> Any:
        # Minimal JSON stub: nothing real, just a placeholder.
        return {}

    async def __aenter__(self) -> "DummyResponse":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return False


class ClientSession:
    """Very small stand-in for aiohttp.ClientSession."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed = False

    async def __aenter__(self) -> "ClientSession":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        await self.close()
        return False

    async def close(self) -> None:
        self._closed = True

    # Common request helpers – all return DummyResponse with no real I/O.
    async def get(self, *args: Any, **kwargs: Any) -> DummyResponse:
        return DummyResponse()

    async def post(self, *args: Any, **kwargs: Any) -> DummyResponse:
        return DummyResponse()

    async def request(self, method: str, *args: Any, **kwargs: Any) -> DummyResponse:
        return DummyResponse()


__all__ = [
    "ClientSession",
    "ClientError",
    "ClientConnectorError",
    "DummyResponse",
]
