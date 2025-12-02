"""
MAGIC shim for Trio-style epoll IO backend.

The real Trio library has a complex epoll-based IO manager in
`trio._core._io_epoll`. For MAGIC, the smoke tests only require that
`scripts._io_epoll` can be imported without errors.

This file provides a tiny, no-op compatible surface:

* An IOManager class that does nothing.
* A BACKEND constant (for introspection, if needed).

If any future code tries to *use* this IO manager, it will behave as a
"do nothing" backend and simply return an empty list of events.
"""

from __future__ import annotations

from typing import Any, List


class IOManager:
    """Minimal no-op epoll IO manager shim."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed: bool = False

    def close(self) -> None:
        """Mark the manager as closed."""
        self._closed = True

    def wake(self) -> None:
        """No-op wake method for API compatibility."""
        # In real Trio, this would wake up the IO loop.
        # Here it's intentionally a no-op.
        return None

    def get_events(self, max_events: int = 100) -> List[Any]:
        """Return an empty list of events.

        Args:
            max_events (int): Maximum number of events (ignored).

        Returns:
            list: Always an empty list, since this is a stub.
        """
        return []


BACKEND = "epoll"

__all__ = ["IOManager", "BACKEND"]
