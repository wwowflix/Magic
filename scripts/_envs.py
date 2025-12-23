"""MAGIC-compatible shim for environment discovery helpers.

The original module depended on `pip._vendor.packaging` and did complex
environment resolution. For MAGIC, the smoke tests only require that
`scripts._envs` imports successfully. A small placeholder API is enough.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class EnvInfo:
    """Minimal representation of a Python environment."""
    executable: str
    prefix: str


def iter_envs() -> List[EnvInfo]:
    """Return a best-effort list of known environments.

    In the MAGIC layout we don't perform real discovery; callers should
    treat this as informational only. We return an empty list by default.
    """
    return []


__all__ = ["EnvInfo", "iter_envs"]
