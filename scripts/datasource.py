"""
MAGIC Week 0: stub for NumPy DataSource examples.

Goal:
- Let "import scripts.datasource" succeed.
- Avoid using np.DataSource (removed in NumPy 2.0).
- Do NOT touch real filesystem or network.
"""

from __future__ import annotations
from typing import Any


class DataSource:
    """
    Minimal placeholder for numpy.lib.npyio.DataSource.

    We accept any arguments but do not perform any I/O.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def open(self, *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("DataSource stub – no real I/O in MAGIC Week 0")


__all__ = ["DataSource"]
