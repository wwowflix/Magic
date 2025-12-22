"""
MAGIC Week 0: safe stub for pandas-style test_config.

Goal:
- Allow "import scripts.test_config" to succeed in smoke tests.
- No actual tests or option registration run at import time.
"""

from __future__ import annotations

__all__: list[str] = []
