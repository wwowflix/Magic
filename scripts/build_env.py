from __future__ import annotations

"""
MAGIC shim for scripts.build_env.

The original module is pip's BuildEnvironment used for isolated sdist/wheel
builds and depends on `pip._vendor.certifi` and other internals.

For MAGIC Week 0 we only need:

- the module to import cleanly
- a BuildEnvironment class with no-op context management
- simple placeholders for requirement installation hooks
"""

from types import TracebackType
from typing import Iterable, List, Optional, Type


class BuildEnvironment:
    """Minimal no-op build environment."""

    def __init__(self) -> None:
        self._installed: List[str] = []

    def __enter__(self) -> "BuildEnvironment":
        # In real pip this would modify environment variables / sys.path.
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        # No-op cleanup in this MAGIC shim.
        self.cleanup()

    def install_requirements(self, requirements: Iterable[str]) -> None:
        """
        Pretend to install build requirements.

        In this shim we simply record them in-memory.
        """
        self._installed.extend(str(r) for r in requirements)

    def cleanup(self) -> None:
        """Reset internal state (no-op for MAGIC)."""
        self._installed.clear()


__all__ = ["BuildEnvironment"]
