from __future__ import annotations

"""
MAGIC socket shim (scripts._socket)

- Wraps stdlib `socket` module.
- Does NOT modify sys.modules["_socket"].
- Does NOT replace the built-in C extension.

It only provides the minimal helpers that scripts._http / scripts._core expect:
    - DEFAULT_SOCKET_OPTION
    - recv_line(sock)
    - send(sock, data)
    - getdefaulttimeout()
    - recv(sock, bufsize)
    - sock_opt(sock, opt, value=None)
"""

import socket as _stdlib_socket
from typing import Union, Optional


# Example default option you can reuse elsewhere
DEFAULT_SOCKET_OPTION = getattr(_stdlib_socket, "SO_REUSEADDR", None)


def recv_line(sock: _stdlib_socket.socket) -> bytes:
    """
    Read a single CRLF-terminated line from the socket.

    This is a simple, blocking implementation that accumulates bytes
    until it sees b"\r\n" or the socket closes.
    """
    data = bytearray()
    while True:
        chunk = sock.recv(1)
        if not chunk:
            # connection closed
            break
        data += chunk
        if len(data) >= 2 and data[-2:] == b"\r\n":
            break
    return bytes(data)


def send(sock: _stdlib_socket.socket, data: Union[str, bytes]) -> int:
    """
    Send data over the socket.

    - Accepts str or bytes.
    - If str, encodes as UTF-8 before sending.
    Returns the number of bytes sent, like sock.send().
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return sock.send(data)


def getdefaulttimeout() -> Optional[float]:
    """
    Thin wrapper around socket.getdefaulttimeout().
    """
    return _stdlib_socket.getdefaulttimeout()


def recv(sock: _stdlib_socket.socket, bufsize: int) -> bytes:
    """
    Thin wrapper around sock.recv(bufsize).
    Provided for compatibility with websocket-client style helpers.
    """
    return sock.recv(bufsize)


def sock_opt(
    sock: _stdlib_socket.socket,
    opt: int,
    value: Optional[int] = None,
) -> Optional[int]:
    """
    Get or set a socket option on SOL_SOCKET.

    - If value is None: returns current option value (getsockopt).
    - If value is not None: sets the option (setsockopt) and returns None.
    """
    if value is None:
        return sock.getsockopt(_stdlib_socket.SOL_SOCKET, opt)
    sock.setsockopt(_stdlib_socket.SOL_SOCKET, opt, value)
    return None


# Re-export a few common attributes from stdlib socket
socket = _stdlib_socket.socket
AF_INET = _stdlib_socket.AF_INET
SOCK_STREAM = _stdlib_socket.SOCK_STREAM

__all__ = [
    "DEFAULT_SOCKET_OPTION",
    "recv_line",
    "send",
    "getdefaulttimeout",
    "recv",
    "sock_opt",
    "socket",
    "AF_INET",
    "SOCK_STREAM",
]
