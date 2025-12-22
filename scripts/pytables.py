"""
MAGIC Week 0: safe stub for pandas-style pytables integration.

Goal:
- Allow "import scripts.pytables" to succeed.
- Avoid importing heavy optional dependencies or registering options.
"""

from __future__ import annotations

try:
    import pandas as _pd  # noqa: F401
except Exception:
    _pd = None  # type: ignore[assignment]

__all__: list[str] = []
