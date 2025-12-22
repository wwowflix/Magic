from __future__ import annotations

"""
MAGIC – Week 0 connectionpool shim.

Goal
----
- Let `import scripts.connectionpool` succeed during global smoke tests.
- Avoid importing urllib3 internals, sockets, or real network logic.
"""

from typing import Any


class ConnectionPool:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ConnectionPool Week0 stub args={self.args!r} kwargs={self.kwargs!r}>"


class HTTPConnectionPool(ConnectionPool):
    pass


class HTTPSConnectionPool(ConnectionPool):
    pass


__all__ = ["ConnectionPool", "HTTPConnectionPool", "HTTPSConnectionPool"]
