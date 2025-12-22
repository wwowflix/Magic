"""
MAGIC Week 0 – Minimal pure socket stub
"""

from __future__ import annotations
from enum import IntEnum
from typing import Any, Optional


# =======================
# Error types
# =======================
class error(OSError):
    pass


class timeout(error):
    pass


# =======================
# Constants needed by urllib3, asyncio, trio
# =======================
AF_UNSPEC = 0
AF_INET = 2
AF_INET6 = 23

SOCK_STREAM = 1
SOCK_DGRAM = 2

IPPROTO_TCP = 6
TCP_NODELAY = 1

AI_PASSIVE = 1
AI_NUMERICHOST = 4

has_ipv6 = True


# =======================
# Timeout helpers
# =======================
_default_timeout: Optional[float] = None


def getdefaulttimeout() -> Optional[float]:
    return _default_timeout


def setdefaulttimeout(value: Optional[float]) -> None:
    global _default_timeout
    _default_timeout = value


# =======================
# Enums (trio requires these!)
# =======================
class AddressFamily(IntEnum):
    AF_UNSPEC = AF_UNSPEC
    AF_INET = AF_INET
    AF_INET6 = AF_INET6


class SocketKind(IntEnum):
    SOCK_STREAM = SOCK_STREAM
    SOCK_DGRAM = SOCK_DGRAM


# =======================
# Minimal dummy socket class
# =======================
class socket:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout = _default_timeout
        self._closed = False

    def settimeout(self, value: Optional[float]) -> None:
        self.timeout = value

    def getsockopt(self, *args: Any, **kwargs: Any) -> int:
        return 0

    def setsockopt(self, *args: Any, **kwargs: Any) -> None:
        pass

    def connect(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("MAGIC socket stub: networking disabled")

    def close(self) -> None:
        self._closed = True

    def makefile(self, *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("MAGIC socket stub: makefile disabled")

    @property
    def family(self) -> int:
        return AF_INET

    @property
    def type(self) -> int:
        return SOCK_STREAM


__all__ = [
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
    "AddressFamily",
    "SocketKind",
    "error",
    "timeout",
    "getdefaulttimeout",
    "setdefaulttimeout",
    "socket",
]
