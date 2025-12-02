"""
MAGIC Week 0: safe stub for pandas-style configTools.

Goal:
- Allow "import scripts.configTools" to succeed.
- Do NOT register any pandas options.
"""

from __future__ import annotations

try:
    import pandas as _pd  # noqa: F401
except Exception:
    _pd = None  # type: ignore[assignment]

__all__: list[str] = []
