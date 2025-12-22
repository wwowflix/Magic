from __future__ import annotations

"""
MAGIC Week 0 shim for websocket helper module `scripts._socket`.

This is NOT the low-level C extension `_socket` from the stdlib.
Instead, it provides the higher-level helpers that the vendored
websocket client code expects:

- DEFAULT_SOCKET_OPTION
- getdefaulttimeout
- recv
- recv_line
- send
- sock_opt

Week 0 goals:
- Imports must succeed (`from ._socket import ...`).
- No real network I/O is required; helpers can be no-op or raise
  clear errors if actually used.
"""

from typing import Any, Iterable, Tuple, Optional
import socket as _socket


# In the real websocket-client, this is a tuple of (level, optname, value)
# pairs applied to sockets. For Week 0, we only need it to exist.
DEFAULT_SOCKET_OPTION: tuple[tuple[int, int, int], ...] = ()


def getdefaulttimeout() -> Optional[float]:
    """
    Return the default socket timeout.

    We delegate to the real stdlib socket.getdefaulttimeout so that
    any code that inspects this value behaves normally.
    """
    return _socket.getdefaulttimeout()


def recv(sock: _socket.socket, bufsize: int, *args: Any, **kwargs: Any) -> bytes:
    """
    Stub for websocket `_socket.recv`.

    Week 0: we refuse real network I/O; if a test actually tries to use this,
    it will see a clear error. Import-time code won't call it.
    """
    raise OSError("MAGIC Week 0 stub: network disabled (_socket.recv)")


def recv_line(sock: _socket.socket, *args: Any, **kwargs: Any) -> bytes:
    """
    Stub for websocket `_socket.recv_line`.

    Again, this is only here so that imports succeed.
    """
    raise OSError("MAGIC Week 0 stub: network disabled (_socket.recv_line)")


def send(sock: _socket.socket, data: bytes, *args: Any, **kwargs: Any) -> int:
    """
    Stub for websocket `_socket.send`.
    """
    raise OSError("MAGIC Week 0 stub: network disabled (_socket.send)")


def sock_opt(sock: _socket.socket) -> None:
    """
    Apply socket options.

    Real implementation would set TCP_NODELAY, etc. For Week 0 we simply
    do nothing; existence of the function is enough for imports.
    """
    return None


__all__ = [
    "DEFAULT_SOCKET_OPTION",
    "getdefaulttimeout",
    "recv",
    "recv_line",
    "send",
    "sock_opt",
]
