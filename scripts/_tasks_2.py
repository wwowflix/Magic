"""MAGIC shim for trio.task-group related helpers."""

from __future__ import annotations


class TaskGroup:
    """Minimal placeholder TaskGroup."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class TaskStatus:
    """Placeholder used by async entrypoints."""
    def started(self, value=None):  # pragma: no cover - shim only
        return None
