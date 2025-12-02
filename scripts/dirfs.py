"""
MAGIC Week 0: stub for scripts.dirfs.

Goal:
- Let "import scripts.dirfs" succeed.
- Provide a minimal DirFS-like object + open_dir helper.
- Do NOT touch the real filesystem at import time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DirFS:
    """
    Very small placeholder for a directory-backed filesystem.

    Week 0:
    - We just store the root path.
    - Methods are no-op / safe defaults.
    """

    root_path: str = "/"

    def open(self, path: str, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("DirFS stub – no real I/O in MAGIC Week 0")

    def listdir(self, path: str = ".") -> list[str]:
        return []

    def exists(self, path: str) -> bool:
        return False


def open_dir(path: str, *args: Any, **kwargs: Any) -> DirFS:
    return DirFS(root_path=path)


__all__ = ["DirFS", "open_dir"]
