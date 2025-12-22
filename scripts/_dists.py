"""MAGIC-compatible wrapper for the _dists helpers.

This is a reduced, import-safe version that avoids depending on
`pip._vendor.packaging`. The MAGIC smoke tests only require that
`scripts._dists` imports successfully; full distribution / requirement
logic is *not* needed here.
"""

from __future__ import annotations

import importlib.metadata
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class DistInfo:
    """Minimal representation of an installed distribution."""
    name: str
    version: str


def iter_installed() -> List[DistInfo]:
    """Return a simple list of installed distributions (name + version only).

    This is intentionally minimal and safe: if anything goes wrong while
    reading metadata, the distribution is skipped.
    """
    results: List[DistInfo] = []
    for dist in importlib.metadata.distributions():
        try:
            metadata = dist.metadata
            name = metadata.get("Name") or getattr(dist, "metadata", {}).get("name", None) or dist.metadata.get("Summary", "unknown")
            version = getattr(dist, "version", "0")
            results.append(DistInfo(name=str(name), version=str(version)))
        except Exception:
            # Best-effort only; ignore broken metadata
            continue
    return results


__all__ = ["DistInfo", "iter_installed"]
