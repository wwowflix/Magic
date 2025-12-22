from __future__ import annotations

"""
MAGIC stub: lightweight replacement for fsspec-based cache mapper.

The original module depended on:
    from fsspec.implementations.local import make_path_posix

For MAGIC Week 0 we only need:
- imports to succeed
- a tiny CacheMapper with a deterministic key + path helper
"""

import os
import hashlib
from typing import Protocol


def make_path_posix(path: str) -> str:
    """
    Minimal stand-in for fsspec.implementations.local.make_path_posix.

    We just convert backslashes to forward slashes.
    """
    return os.fspath(path).replace("\\", "/")


class CacheMapper(Protocol):
    """
    Very small protocol for cache mappers.

    This matches the rough shape of the original API so type hints
    or simple call sites keep working.
    """

    def key_for_path(self, path: str) -> str:
        ...

    def cache_path(self, path: str) -> str:
        ...


class SimpleCacheMapper:
    """
    Default mapper used in the MAGIC stub.

    - normalises path to POSIX style
    - hashes it with SHA-256 to produce a stable key
    """

    def key_for_path(self, path: str) -> str:
        norm = make_path_posix(path)
        return hashlib.sha256(norm.encode("utf-8")).hexdigest()

    def cache_path(self, path: str) -> str:
        # In a real implementation this might prepend a cache directory.
        # For Week 0 we just return the key.
        return self.key_for_path(path)


# Module-level default mapper, similar to how the original module is used.
DEFAULT_MAPPER = SimpleCacheMapper()
