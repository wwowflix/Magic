from __future__ import annotations

"""
MAGIC – Week 0 util.retry shim.

Goal
----
- Provide a minimal Retry object so `scripts.connectionpool` imports cleanly.
- We do NOT implement real retry behaviour in Week 0.
"""

from typing import Any, Iterable, Optional, TypeVar, Type

_T = TypeVar("_T", bound="Retry")


class Retry:
    """
    Very loose stand-in for urllib3.util.retry.Retry.

    For Week 0 we only need:
    - the class to exist
    - it to accept any arguments
    - basic helpers (`new`, `from_int`) so any import-time wiring doesn't crash.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Store everything for debug visibility, but don't enforce a schema.
        self.args = args
        self.kwargs = dict(kwargs)

    def new(self: _T, **kw: Any) -> _T:
        """
        Week 0 stub: return a shallow "copy" with updated kwargs.
        """
        merged = dict(getattr(self, "kwargs", {}))
        merged.update(kw)
        clone = type(self)(*getattr(self, "args", ()), **merged)
        return clone

    @classmethod
    def from_int(cls: Type[_T], retries: int = 3, **kw: Any) -> _T:
        """
        Week 0 stub loosely compatible with urllib3.util.Retry.from_int.
        """
        merged = dict(kw)
        merged.setdefault("total", retries)
        return cls(**merged)  # type: ignore[arg-type]


__all__ = ["Retry"]
