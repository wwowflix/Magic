"""
MAGIC-safe shim for scripts._generated_io_epoll.

Upstream wires epoll I/O into the run loop. For MAGIC smokes, we only
need this module to import safely, not to run real epoll logic.
"""

from __future__ import annotations
from typing import Any

class GeneratedIOEpoll:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def close(self) -> None: ...
    def fileno(self) -> int: return -1  # sentinel

DEFAULT_IO = GeneratedIOEpoll()

__all__ = ["GeneratedIOEpoll", "DEFAULT_IO"]
