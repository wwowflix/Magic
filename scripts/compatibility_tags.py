from __future__ import annotations

"""
Week 0 stub for `scripts.compatibility_tags`.

The original module depends on `pip._vendor.packaging.tags` to generate
PEP 425 compatibility tags. For MAGIC Week 0 smoke-import tests we only
need this module to import cleanly, not to compute real tags.
"""

from dataclasses import dataclass
from typing import List, Tuple

PythonVersion = Tuple[int, int]


@dataclass(frozen=True)
class Tag:
    """Minimal stand-in for a wheel compatibility tag."""
    interpreter: str
    abi: str
    platform: str


def interpreter_name() -> str:
    """Return a dummy interpreter name."""
    return "py"


def interpreter_version() -> str:
    """Return a dummy interpreter version string."""
    return "0"


def compatible_tags(*_args, **_kwargs) -> List[Tag]:
    """Return an empty list of tags in the Week 0 stub."""
    return []


def cpython_tags(*_args, **_kwargs) -> List[Tag]:
    """Return an empty list of CPython tags in the Week 0 stub."""
    return []


def generic_tags(*_args, **_kwargs) -> List[Tag]:
    """Return an empty list of generic tags in the Week 0 stub."""
    return []


def mac_platforms(*_args, **_kwargs) -> List[str]:
    """Return an empty list of macOS platform tags in the Week 0 stub."""
    return []
