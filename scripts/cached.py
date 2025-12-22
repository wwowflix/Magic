from __future__ import annotations

"""
MAGIC stub: replacement for a cached filesystem wrapper that depended on fsspec.

The original module imported:

    from fsspec import AbstractFileSystem, filesystem

and implemented a caching filesystem on top.

For MAGIC Week 0 we only need:

- imports to succeed
- a tiny AbstractFileSystem placeholder
- a filesystem() factory that returns a dummy FS
"""

from typing import Any


class AbstractFileSystem:
    """Very small stand-in for fsspec.AbstractFileSystem."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Just keep the storage options around for introspection if needed.
        self.storage_options = kwargs

    def open(self, path: str, mode: str = "rb", *args: Any, **kwargs: Any):
        """
        Minimal open() placeholder.

        In real code this would return a file-like object.
        For MAGIC Week 0 we raise NotImplementedError so any accidental
        runtime usage fails loudly instead of doing something unsafe.
        """
        raise NotImplementedError("MAGIC stub filesystem does not implement open()")


class DummyFileSystem(AbstractFileSystem):
    """Simple concrete subclass used by the filesystem() helper."""
    pass


def filesystem(protocol: str, **storage_options: Any) -> AbstractFileSystem:
    """
    Minimal stand-in for fsspec.filesystem(...).

    We ignore the protocol and return a DummyFileSystem with the given
    storage options.
    """
    return DummyFileSystem(**storage_options)
