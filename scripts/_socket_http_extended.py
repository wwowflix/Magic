"""
MAGIC – Extended WebSocket / HTTP socket shim.

This module exists to provide a stable surface for:
- DEFAULT_SOCKET_OPTION
- recv_line()
- send_bytes()

It is NOT a full HTTP/WebSocket implementation – just enough
for MAGIC imports and basic runtime to stay stable.
"""

from __future__ import annotations

from typing import Tuple, Any
import socket


# A safe default socket option tuple commonly used by network libs.
# (family, type, proto) is not strictly required here; we just mirror
# the common SOL_SOCKET/SO_REUSEADDR pattern as a placeholder.
DEFAULT_SOCKET_OPTION: Tuple[int, int, int] = (
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1,
)


def recv_line(sock: Any, limit: int = 65536) -> bytes:
    """
    Read a single line (ending with b"\\n") from the given socket-like object.

    - Tries sock.recv(1) in a loop.
    - Stops when newline or EOF is reached, or when `limit` is exceeded.
    - If the object does not support recv(), returns b"" gracefully.
    """
    if not hasattr(sock, "recv"):
        # Not a real socket – fail soft but safe.
        return b""

    chunks: list[bytes] = []
    total = 0

    while total < limit:
        chunk = sock.recv(1)
        if not chunk:
            # EOF
            break
        chunks.append(chunk)
        total += 1
        if chunk == b"\n":
            break

    return b"".join(chunks)


def send_bytes(sock: Any, data: bytes) -> int:
    """
    Send all bytes to a socket-like object.

    - Prefer sock.sendall() if present.
    - Fallback to sock.send() in a loop.
    - If object only has write(), use that as a best-effort fallback.

    Returns the total number of bytes *attempted* to send.
    """
    if data is None:
        return 0

    # Prefer sendall if available (typical socket interface)
    if hasattr(sock, "sendall"):
        sock.sendall(data)
        return len(data)

    # Fallback: send loop (classic low-level socket)
    if hasattr(sock, "send"):
        view = memoryview(data)
        total = 0
        while total < len(view):
            sent = sock.send(view[total:])
            if sent is None:
                # Some implementations return None; treat as no progress
                break
            if sent == 0:
                # Connection broken
                break
            total += sent
        return total

    # Very last fallback: file-like write()
    if hasattr(sock, "write"):
        sock.write(data)
        return len(data)

    # No known way to send → do nothing but stay safe.
    return 0
