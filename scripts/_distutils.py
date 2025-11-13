"""MAGIC-compatible wrapper for the _distutils helpers.

This is a reduced, import-safe version that avoids depending on
`pip._internal`. The MAGIC smoke tests only require that
`scripts._distutils` imports successfully; full installation scheme
logic is *not* needed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Scheme:
    """Minimal stand-in for pip's Scheme object."""
    platlib: str = ""
    purelib: str = ""
    headers: str = ""
    scripts: str = ""
    data: str = ""


def get_scheme(distribution: str, user: Optional[bool] = None) -> Scheme:
    """Return a dummy Scheme for the given distribution.

    For MAGIC we don't compute real install paths; this is just a
    placeholder to satisfy imports in any consumer code.
    """
    return Scheme()


__all__ = ["Scheme", "get_scheme"]
