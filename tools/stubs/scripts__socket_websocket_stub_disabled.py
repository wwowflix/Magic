"""
MAGIC Week 0: tiny compatibility shim for websocket's _http module.

We DO NOT replace the stdlib socket.
We just expose:
- DEFAULT_SOCKET_OPTION
- recv_line(sock)
- send(sock, data)

All real socket behavior comes from the standard library.
"""

from __future__ import annotations

from typing import Any
import socket as _stdlib_socket


# ==========================
# Default socket option
# ==========================
# This matches what websocket expects: (IPPROTO_TCP, TCP_NODELAY, 1)
DEFAULT_SOCKET_OPTION = (
    _stdlib_socket.IPPROTO_TCP,
    _stdlib_socket.TCP_NODELAY,
    1,
)


# ==========================
# Minimal helpers
# ==========================
def recv_line(sock: Any) -> bytes:
    """
    Minimal recv_line used by scripts._http to read HTTP headers.

    Reads until b"\\n" or EOF. This is intentionally small and only used
    for import-time / header parsing flows in tests.
    """
    data = bytearray()
    while True:
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
        if chunk == b"\\n":
            break
    return bytes(data)


def send(sock: Any, data: bytes | str) -> int:
    """
    Thin wrapper around sock.send().

    Allows both bytes and str, encoding str as UTF-8.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return sock.send(data)


__all__ = ["DEFAULT_SOCKET_OPTION", "recv_line", "send"]
