from __future__ import annotations

"""
MAGIC shim for scripts.build_tracker.

The original module tracks in-progress builds in pip and depends on
`pip._internal.models.link.Link`.

For MAGIC Week 0 we only need:

- the module to import cleanly
- a BuildTracker context manager with no-op / in-memory tracking
"""

from types import TracebackType
from typing import Dict, Optional, Set, Type


class BuildTracker:
    """
    Minimal no-op build tracker.

    Tracks projects by a simple string key; does not touch the filesystem.
    """

    def __init__(self) -> None:
        self._projects: Set[str] = set()

    def __enter__(self) -> "BuildTracker":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.cleanup()

    def add(self, project: str) -> None:
        """Register a project as being built."""
        self._projects.add(str(project))

    def remove(self, project: str) -> None:
        """Remove a project from the tracker."""
        self._projects.discard(str(project))

    def cleanup(self) -> None:
        """Clear all tracked projects."""
        self._projects.clear()

    @property
    def projects(self) -> Set[str]:
        """Return a snapshot of all tracked projects."""
        return set(self._projects)


__all__ = ["BuildTracker"]
