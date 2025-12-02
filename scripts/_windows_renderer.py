from __future__ import annotations

"""
MAGIC shim for rich-style Windows console renderer on Windows.

We do NOT depend on `pip._vendor.rich` here; this file only provides
a couple of tiny placeholder classes and helpers so that imports
succeed during smoke tests.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class WindowsCoordinates:
    x: int = 0
    y: int = 0


class LegacyWindowsTerm:
    """
    Ultra-minimal stand-in for a Windows terminal description.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.size: Tuple[int, int] = (80, 25)

    def get_console_size(self) -> Tuple[int, int]:
        return self.size


def get_console() -> LegacyWindowsTerm:
    """
    Return a dummy LegacyWindowsTerm instance.

    The real implementation would talk to the Windows console API,
    but MAGIC only needs an import-safe placeholder.
    """
    return LegacyWindowsTerm()
