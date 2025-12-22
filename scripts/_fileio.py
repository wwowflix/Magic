"""MAGIC-compatible shim for file I/O helpers.

The original module depended on a higher-level `to_thread` helper via a
relative import. For MAGIC, the smoke tests only require that
`scripts._fileio` imports successfully. A small synchronous helper API
is sufficient.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def read_text(path: PathLike, encoding: str = "utf-8") -> str:
    """Read a text file and return its contents."""
    return Path(path).read_text(encoding=encoding)


def write_text(path: PathLike, data: str, encoding: str = "utf-8") -> None:
    """Write text data to a file, creating parents if needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding=encoding)


__all__ = ["read_text", "write_text", "PathLike"]
