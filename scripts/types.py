from __future__ import annotations

"""
MAGIC – Week 0 scripts.types shim.

Goal
----
- Provide a `scripts.types` module so vendored code doing
  `from scripts import types` or `from .types import *` works.
- Re-export everything from the stdlib `types` module.
"""

from types import *  # type: ignore

__all__ = [name for name in globals().keys() if not name.startswith("_")]
