"""
MAGIC stub: lightweight filesystem helper for "arrow"-style paths.

The original module depends on fsspec.AbstractFileSystem and cloud backends.
For MAGIC we only need a very small, local-files-only helper so that imports
succeed and basic I/O can be exercised in tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional
import os


@dataclass
class ArrowFileSystem:
    """
    Tiny stand-in for an AbstractFileSystem-like object.

    It only operates on the local filesystem rooted at base_path (if given).
    """

    base_path: Optional[str] = None

    def _resolve(self, path: str) -> str:
        if self.base_path:
            return os.path.join(self.base_path, path)
        return path

    def open(self, path: str, mode: str = "rb"):
        return open(self._resolve(path), mode)

    def exists(self, path: str) -> bool:
        return os.path.exists(self._resolve(path))

    def ls(self, path: str = ".") -> list[str]:
        full = self._resolve(path)
        try:
            return sorted(os.listdir(full))
        except FileNotFoundError:
            return []

    def walk(self, path: str = ".") -> Iterator[tuple[str, list[str], list[str]]]:
        full = self._resolve(path)
        if not os.path.isdir(full):
            return iter(())
        return os.walk(full)


def get_local_filesystem(base_path: Optional[str] = None) -> ArrowFileSystem:
    """
    Convenience helper to construct a local ArrowFileSystem.
    """
    return ArrowFileSystem(base_path=base_path)
