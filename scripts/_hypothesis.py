"""
MAGIC stub for scripts._hypothesis

The original implementation used the external `hypothesis` library:

    from hypothesis import strategies as st

For MAGIC we only need:
- The module to import cleanly.
- A `st` object with simple, predictable behaviour if it is used.

This shim avoids importing the real library and instead exposes a tiny,
in-memory stand-in that mimics the public shape of `hypothesis.strategies`.
"""

from __future__ import annotations

from typing import Any, Dict


class _DummyStrategy:
    """Very small stand-in for a Hypothesis strategy."""

    def __init__(self, name: str, meta: Dict[str, Any] | None = None) -> None:
        self.name = name
        self.meta = meta or {}

    def example(self) -> Any:
        """
        Return a deterministic placeholder value.

        We intentionally do NOT try to generate real randomized data here.
        """
        return {
            "strategy": self.name,
            "meta": self.meta,
        }

    # Make it slightly more flexible if called like a function
    def __call__(self, *args: Any, **kwargs: Any) -> "_DummyStrategy":
        meta = dict(self.meta)
        if args:
            meta["args"] = args
        if kwargs:
            meta["kwargs"] = kwargs
        return _DummyStrategy(self.name, meta)


class _DummyStrategies:
    """
    Minimal object that roughly looks like `hypothesis.strategies`.

    Only a handful of helpers are defined explicitly; everything else
    falls back to a generic `_DummyStrategy`.
    """

    # Common helpers that some code might expect
    def integers(self, *args: Any, **kwargs: Any) -> _DummyStrategy:
        return _DummyStrategy("integers", {"args": args, "kwargs": kwargs})

    def text(self, *args: Any, **kwargs: Any) -> _DummyStrategy:
        return _DummyStrategy("text", {"args": args, "kwargs": kwargs})

    def booleans(self) -> _DummyStrategy:
        return _DummyStrategy("booleans")

    def floats(self, *args: Any, **kwargs: Any) -> _DummyStrategy:
        return _DummyStrategy("floats", {"args": args, "kwargs": kwargs})

    def just(self, value: Any) -> _DummyStrategy:
        return _DummyStrategy("just", {"value": value})

    # Generic fallback: any unknown attribute → dummy strategy
    def __getattr__(self, name: str) -> _DummyStrategy:
        return _DummyStrategy(name)


# Public shim that callers can use like `st.integers()`, `st.text()`, etc.
st = _DummyStrategies()

__all__ = ["st", "_DummyStrategy", "_DummyStrategies"]
