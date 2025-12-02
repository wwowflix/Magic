"""MAGIC shim for numpy.random._random-like helpers.

NumPy 2 removed np.unicode_, so we replace the vendored module with a
small compatibility wrapper.
"""

from __future__ import annotations

from typing import Any

try:
    from numpy.random.mtrand import RandomState  # type: ignore[import]
except Exception:  # pragma: no cover
    class RandomState:  # type: ignore[no-redef]
        def __init__(self, seed: Any | None = None) -> None:
            self.seed = seed

        def __repr__(self) -> str:
            return f"RandomState(seed={self.seed!r})"


__all__ = ["RandomState"]
