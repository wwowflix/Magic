from __future__ import annotations

"""
MAGIC stub: safe placeholder for pandas Categorical / category helpers.

Week 0 goal:
- Allow `import scripts.category` to succeed.
- Avoid importing pandas internals that mismatch versions.

If a future MAGIC phase needs real category logic,
it can be implemented in a dedicated, tested module.
"""


class CategoricalIndex:
    """Very small placeholder for a categorical index type."""
    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover
        self._data = list(args) if args else []

    def __repr__(self) -> str:  # pragma: no cover
        return f"MAGIC-CategoricalIndex(len={len(self._data)})"
