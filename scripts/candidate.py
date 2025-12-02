from __future__ import annotations

"""
MAGIC stub: replacement for pip's InstallationCandidate helper.

The original module depended on `pip._vendor.packaging.version`.
For MAGIC Week 0 we only need:

- imports to succeed
- a simple data holder for a candidate (name, version, link)
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InstallationCandidate:
    name: str
    version: str
    link: Any | None = None

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name}=={self.version}"
