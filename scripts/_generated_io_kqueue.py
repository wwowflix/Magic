"""
MAGIC-safe shim for scripts._generated_io_kqueue.

Upstream wires kqueue I/O into the run loop. For MAGIC smokes, we only
need this module to import safely, not to run real kqueue logic.
"""

from __future__ import annotations
from typing import Any

class GeneratedIOKqueue:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def close(self) -> None: ...
    def fileno(self) -> int: return -1  # sentinel

DEFAULT_IO = GeneratedIOKqueue()

__all__ = ["GeneratedIOKqueue", "DEFAULT_IO"]
