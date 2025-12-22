from __future__ import annotations

"""
MAGIC stub: lightweight replacement for a vendored `bazaar` module.

The original file depended on `pip._internal.utils.misc.HiddenText` and
`display_path`, which may not be available or stable in this environment.

For MAGIC Week 0 we only need:
- the module to import cleanly
- a couple of simple helpers that look like the ones pip exposes.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class HiddenText:
    """
    Minimal stand-in for pip's HiddenText.

    In pip, this wraps a secret value with a redacted display version.
    For our purposes, we just keep both and show the redacted value if present.
    """

    value: str
    redacted: str | None = None

    def __str__(self) -> str:  # pragma: no cover
        return self.redacted or self.value


def display_path(path: Any) -> str:
    """
    Minimal stand-in for pip's display_path.

    Just converts the given path-ish object to a string.
    """
    return str(path)


__all__ = ["HiddenText", "display_path"]
