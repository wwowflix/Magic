"""MAGIC shim for trio._streams."""
from __future__ import annotations

class MemorySendStream:
    async def send_all(self, data: bytes) -> None:  # pragma: no cover
        return None

class MemoryReceiveStream:
    async def receive_some(self, max_bytes: int) -> bytes:  # pragma: no cover
        return b""
