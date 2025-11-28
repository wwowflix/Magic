"""
MAGIC Week 0 shim for top-level `cryptography` package.

Goal:
- Allow `from cryptography import utils` to work.
- We only provide a minimal `utils` module good enough for scripts.concatkdf.
"""

from __future__ import annotations

from . import utils  # re-export

__all__ = ["utils"]
