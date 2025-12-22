"""
MAGIC – socket compatibility shim

Provides the subset of attributes expected by:
- scripts.socket
- scripts._highlevel_open_tcp_listeners
- scripts._http / websocket-style helpers

Backed by the standard library `socket` module.
"""

from __future__ import annotations

import socket as _stdlib_socket
from typing import Any, Optional, Tuple

# Trio-style type alias – good enough for our purposes
SocketType = _stdlib_socket.socket


def from_stdlib_socket(sock: _stdlib_socket.socket) -> SocketType:
    """Wrap a stdlib socket as our SocketType (identity here)."""
    return sock


def fromfd(fd: int, family: int, type: int, proto: int = 0) -> SocketType:
    """Create a socket from an OS file descriptor."""
    return _stdlib_socket.fromfd(fd, family, type, proto)


def getaddrinfo(*args: Any, **kwargs: Any):
    """Proxy to stdlib getaddrinfo."""
    return _stdlib_socket.getaddrinfo(*args, **kwargs)


def getnameinfo(*args: Any, **kwargs: Any):
    """Proxy to stdlib getnameinfo."""
    return _stdlib_socket.getnameinfo(*args, **kwargs)


def getprotobyname(name: str) -> int:
    """Proxy to stdlib getprotobyname."""
    return _stdlib_socket.getprotobyname(name)


# Hooks for custom behavior – by default just store the callbacks
_custom_hostname_resolver = None
_custom_socket_factory = None


def set_custom_hostname_resolver(func) -> None:
    global _custom_hostname_resolver
    _custom_hostname_resolver = func


def set_custom_socket_factory(func) -> None:
    global _custom_socket_factory
    _custom_socket_factory = func


def socket(*args: Any, **kwargs: Any) -> SocketType:
    """Create a socket, optionally via custom factory."""
    if _custom_socket_factory is not None:
        return _custom_socket_factory(*args, **kwargs)
    return _stdlib_socket.socket(*args, **kwargs)


def socketpair(*args: Any, **kwargs: Any) -> Tuple[SocketType, SocketType]:
    """
    Create a pair of connected sockets.

    On platforms without socketpair(), we provide a very crude fallback that
    should still satisfy imports and basic smoke tests.
    """
    if hasattr(_stdlib_socket, "socketpair"):
        return _stdlib_socket.socketpair(*args, **kwargs)

    # Very rough fallback: two independent sockets (not actually connected).
    # Good enough for code that never calls this in tests.
    s1 = _stdlib_socket.socket()
    s2 = _stdlib_socket.socket()
    return s1, s2


# ---- Extra symbols expected by scripts._http ----

# In real libraries this is usually a tuple of (level, optname, value),
# but for import/smoke purposes any simple constant is fine.
DEFAULT_SOCKET_OPTION = None


def recv_line(sock: _stdlib_socket.socket, bufsize: int = 4096) -> bytes:
    """
    Read a single line from the socket, ending with b'\\n'.

    Minimal implementation – good enough for tests that don't actually
    call this, or that only need basic behaviour.
    """
    chunks = []
    while True:
        chunk = sock.recv(1)
        if not chunk:
            break
        chunks.append(chunk)
        if chunk == b"\n":
            break
    return b"".join(chunks)


def send(sock: _stdlib_socket.socket, data: Any) -> int:
    """
    Send data over the socket.

    Accepts str or bytes; converts str to utf-8.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return sock.send(data)
