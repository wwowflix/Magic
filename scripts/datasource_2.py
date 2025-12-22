"""
MAGIC Week 0: stub for datasource_2.

Goal:
- Let "import scripts.datasource_2" succeed.
- Re-export DataSource from scripts.datasource.
- Avoid calling DataSource(...) at import time.
"""

from __future__ import annotations

from .datasource import DataSource

__all__ = ["DataSource"]
