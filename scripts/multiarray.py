"""
MAGIC shim for scripts.multiarray.

Goal:
- Provide `dtype`, `array`, and `ndarray` so that scripts._internal
  can import them without errors.
- Prefer the real NumPy types if NumPy is installed.
- Fall back to lightweight placeholders if NumPy is unavailable.
"""

from __future__ import annotations

from typing import Any

# Try to use real numpy types if available
try:  # pragma: no cover - optional dependency
    import numpy as _np  # type: ignore[import]

    dtype = _np.dtype               # type: ignore[assignment]
    array = _np.array               # type: ignore[assignment]
    ndarray = _np.ndarray           # type: ignore[assignment]

except Exception:
    # Fallback: very simple stand-in implementations

    class ndarray(list):
        """
        Minimal stand-in for numpy.ndarray.

        This only needs to be "list-like" enough so that code does not
        crash when it receives an `ndarray` instance. We don't try to
        emulate real NumPy behaviour here.
        """
        # You can add more helpers if ever needed
        pass

    def array(obj: Any, dtype: Any | None = None, **_: Any) -> "ndarray":
        """
        Fallback `array` constructor: just wrap `obj` in our dummy ndarray.
        """
        if isinstance(obj, ndarray):
            return obj
        # Make a shallow copy in list form
        try:
            return ndarray(obj)  # type: ignore[arg-type]
        except TypeError:
            # Not iterable, treat as scalar
            return ndarray([obj])

    class _FakeDType:
        """
        Minimal dtype stand-in used when NumPy is not available.
        """

        def __init__(self, name: str) -> None:
            self.name = str(name)

        def __repr__(self) -> str:  # pragma: no cover - trivial
            return f"dtype({self.name!r})"

        def __str__(self) -> str:  # pragma: no cover - trivial
            return self.name

    def dtype(obj: Any) -> "_FakeDType":
        """
        Fallback `dtype` constructor: just records the given object as a name.
        """
        return _FakeDType(str(obj))


__all__ = ["dtype", "array", "ndarray"]
