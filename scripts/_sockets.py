"""
MAGIC shim for socket helpers.

Goal (Week 0 – Stage 1):
- Provide a stable import surface for tests that import `scripts._sockets`.
- Avoid fragile logic here; delegate real behavior to stdlib where possible.
"""

from __future__ import annotations

import socket
from typing import Protocol, Any


class SupportsSocket(Protocol):
    """Minimal protocol for typed socket-like objects."""

    def fileno(self) -> int:
        ...

    def close(self) -> None:
        ...


DEFAULT_SOCKET_OPTION: Any = None


def ensure_connected(sock: socket.socket) -> socket.socket:
    if not isinstance(sock, socket.socket):
        raise TypeError(f"Expected socket.socket, got {type(sock)!r}")
    return sock


__all__ = [
    "socket",
    "SupportsSocket",
    "DEFAULT_SOCKET_OPTION",
    "ensure_connected",
]
