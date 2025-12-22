"""
MAGIC Week 0: minimal socket stub for import-only use.

We don't perform real networking here. The goal is only:
- Make 'import socket' and 'from socket import ...' succeed.
- Provide attributes used by urllib3 / asyncio / trio during *import time*.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Any, Optional


# ===========================
# Error types (like stdlib)
# ===========================
class error(OSError):
    """Generic socket error (stub)."""


class timeout(error):
    """Timeout error (stub)."""


# ===========================
# Basic constants
# ===========================
AF_UNSPEC = 0
AF_INET = 2
AF_INET6 = 23

SOCK_STREAM = 1
SOCK_DGRAM = 2

IPPROTO_TCP = 6
TCP_NODELAY = 1

# DNS / getaddrinfo flags used by trio
AI_PASSIVE = 1
AI_NUMERICHOST = 4  # actual value doesn't matter for tests

# urllib3 / others check this
has_ipv6: bool = True


# ===========================
# Default timeout helpers
# ===========================
_default_timeout: Optional[float] = None


def getdefaulttimeout() -> Optional[float]:
    return _default_timeout


def setdefaulttimeout(value: Optional[float]) -> None:
    global _default_timeout
    _default_timeout = value


# ===========================
# Enum types (for trio)
# ===========================
class AddressFamily(IntEnum):
    AF_UNSPEC = AF_UNSPEC
    AF_INET = AF_INET
    AF_INET6 = AF_INET6


class SocketKind(IntEnum):
    SOCK_STREAM = SOCK_STREAM
    SOCK_DGRAM = SOCK_DGRAM


# ===========================
# Minimal socket class
# ===========================
class socket:
    """
    Dummy socket class.

    Enough to satisfy type/attribute access during urllib3/asyncio/trio import and
    connection setup. Any real networking call will raise RuntimeError so we
    don't accidentally talk to the network from tests.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout = _default_timeout
        self._closed = False

    # Methods urllib3 / http.client may touch
    def settimeout(self, value: Optional[float]) -> None:
        self.timeout = value

    def getsockopt(self, *args: Any, **kwargs: Any) -> int:
        return 0

    def setsockopt(self, *args: Any, **kwargs: Any) -> None:
        # In tests we don't care about socket options
        pass

    def connect(self, *args: Any, **kwargs: Any) -> None:
        # If we ever hit this in Week 0, something is trying real I/O.
        raise RuntimeError("MAGIC socket stub: real networking disabled in Week 0")

    def close(self) -> None:
        self._closed = True

    def makefile(self, *args: Any, **kwargs: Any) -> Any:
        # http.client may try to call this if we ever did real I/O.
        raise RuntimeError("MAGIC socket stub: makefile() not available")

    # For safety if something checks these
    @property
    def family(self) -> int:
        return AF_INET

    @property
    def type(self) -> int:
        return SOCK_STREAM


__all__ = [
    # constants
    "AF_UNSPEC",
    "AF_INET",
    "AF_INET6",
    "SOCK_STREAM",
    "SOCK_DGRAM",
    "IPPROTO_TCP",
    "TCP_NODELAY",
    "AI_PASSIVE",
    "AI_NUMERICHOST",
    "has_ipv6",
    # types
    "error",
    "timeout",
    "AddressFamily",
    "SocketKind",
    # helpers
    "getdefaulttimeout",
    "setdefaulttimeout",
    # class
    "socket",
]
