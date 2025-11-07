"""MAGIC shim: minimal socket options typing for base_connection imports."""

from typing import Any, Iterable, Tuple

# Iterable of 3-tuples: (level, optname, value)
# This matches typical socket.setsockopt call patterns.
_TYPE_SOCKET_OPTIONS = Iterable[Tuple[int, int, Any]]

__all__ = ["_TYPE_SOCKET_OPTIONS"]
