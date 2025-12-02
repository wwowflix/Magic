"""
MAGIC Week 0: stub for scripts.database (distlib-style database).

Goal:
- Let "import scripts.database" succeed.
- Avoid touching real installation metadata or zipimport.
"""

from __future__ import annotations
from typing import Any


class Database:
    """
    Minimal placeholder for distlib.database.DistributionPath / Database.

    We just store args; no real behaviour in Week 0.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Database stub args={self.args!r} kwargs={self.kwargs!r}>"

__all__ = ["Database"]
