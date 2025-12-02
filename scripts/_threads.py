"""MAGIC shim for trio.thread helpers."""

from __future__ import annotations


def start_thread_soon(fn, *args, **kwargs):  # pragma: no cover - shim
    """Fire-and-forget thread runner placeholder."""
    # In MAGIC tests we do nothing; this just satisfies imports.
    return None
