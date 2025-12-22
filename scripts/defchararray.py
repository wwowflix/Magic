"""
MAGIC Week 0: stub for scripts.defchararray.

Goal:
- Allow "import scripts.defchararray" to succeed.
- Provide minimal stand-ins so nothing crashes at import time.
- No real NumPy string array logic implemented.
"""

from __future__ import annotations
from typing import Any

class CharArray:
    """
    Minimal placeholder for NumPy's chararray/string operations.
    Week 0: does nothing, only exists so imports do not fail.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<CharArray stub args={self.args!r} kwargs={self.kwargs!r}>"

# Common alias NumPy exposes
def array(*args: Any, **kwargs: Any) -> CharArray:
    return CharArray(*args, **kwargs)

__all__ = ["CharArray", "array"]
