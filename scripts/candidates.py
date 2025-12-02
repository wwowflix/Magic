from __future__ import annotations

"""
MAGIC stub: replacement for pip's candidates helper module.

The original module depended on `pip._vendor.packaging.utils`.
For MAGIC Week 0 we only need:

- imports to succeed
- a simple NormalizedName type + canonicalize_name()
- a few small helpers that work on InstallationCandidate objects
"""

from dataclasses import dataclass
from typing import Iterable, List, Optional

from .candidate import InstallationCandidate

# In real pip this is a distinct type; for our purposes a plain str is fine.
NormalizedName = str


def canonicalize_name(name: str) -> NormalizedName:
    """Very small stand-in: normalize by lowercasing and stripping spaces."""
    return name.strip().lower()


@dataclass(frozen=True)
class CandidatePreferences:
    """Tiny preferences container used by higher-level code."""
    allow_yanked: bool = False


def as_list(candidates: Iterable[InstallationCandidate]) -> List[InstallationCandidate]:
    """Return candidates as a concrete list."""
    return list(candidates)


def pick_best(candidates: Iterable[InstallationCandidate]) -> Optional[InstallationCandidate]:
    """
    Very small helper to pick a 'best' candidate by version string.

    This is intentionally simple; for MAGIC Week 0 we only care that the
    function exists and behaves deterministically.
    """
    best: Optional[InstallationCandidate] = None
    for c in candidates:
        if best is None or (c.version or "") > (best.version or ""):
            best = c
    return best
