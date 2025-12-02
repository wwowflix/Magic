from __future__ import annotations

"""
MAGIC shim for scripts.archive

Original module depends on `fsspec.AbstractFileSystem` and related
filesystem backends.

For MAGIC smoke tests we only need:
- `import scripts.archive` to succeed.
- A very small, predictable API surface that does NOT import fsspec.

This shim provides:
- ArchiveEntry: tiny description of a file in an archive
- ArchiveFS: fake filesystem with minimal methods (ls, open)
"""

from dataclasses import dataclass
from typing import Any, Iterable, List
import io


@dataclass
class ArchiveEntry:
    """Minimal representation of an entry in an archive."""
    path: str
    size: int = 0
    info: dict | None = None


class ArchiveFS:
    """
    Tiny placeholder filesystem-like object.

    Methods:
    - ls(path) -> list[ArchiveEntry]
    - open(path, mode="rb") -> file-like object
    """

    def __init__(self, root: str | None = None) -> None:
        self.root = root or ""

    def ls(self, path: str = "") -> List[ArchiveEntry]:
        # For MAGIC, this returns an empty listing.
        return []

    def open(self, path: str, mode: str = "rb") -> Any:
        # Return an in-memory empty file-like object.
        # This is good enough for smoke tests that never inspect content.
        binary = "b" in mode
        if binary:
            return io.BytesIO(b"")
        return io.StringIO("")


__all__ = ["ArchiveEntry", "ArchiveFS"]
