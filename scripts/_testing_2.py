"""MAGIC shim for async testing helpers."""

from __future__ import annotations


async def run_async_test(fn, *args, **kwargs):  # pragma: no cover - shim
    """Call an async test function if provided."""
    return await fn(*args, **kwargs)
