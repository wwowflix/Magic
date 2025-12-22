from __future__ import annotations

"""
MAGIC shim for scripts.apply

Original module depends heavily on pandas internals
(pandas.core.construction, NDFrame.apply logic, etc.).

For MAGIC smoke tests we only need:
- `import scripts.apply` to succeed.
- A very small, predictable API surface that does not pull in pandas.

This shim provides:
- ApplyResult: tiny container for results
- apply(obj, func, axis=0, *args, **kwargs): minimal no-op wrapper
"""


from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ApplyResult:
    """Minimal container for an apply-like result."""
    value: Any


def apply(obj: Any, func: Callable[[Any], Any], axis: int = 0, *args: Any, **kwargs: Any) -> ApplyResult:
    """
    Trivial apply implementation for MAGIC.

    - Ignores axis/args/kwargs semantics.
    - Simply calls `func(obj)` and wraps the result.
    """
    result = func(obj)
    return ApplyResult(value=result)


__all__ = ["ApplyResult", "apply"]
