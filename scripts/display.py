"""
MAGIC Week 0: safe stub for pandas-style display module.

Goal:
- Allow "import scripts.display" to succeed.
- Do NOT register any pandas options or change global display options.
"""

from __future__ import annotations

try:
    import pandas as _pd  # noqa: F401
except Exception:
    _pd = None  # type: ignore[assignment]

__all__: list[str] = []
