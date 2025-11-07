from __future__ import annotations

"""MAGIC shim: minimal timeout typing/sentinel for base_connection imports."""
from typing import Optional


# Sentinel value some stdlib-inspired modules check against
class _Sentinel:
    def __repr__(self) -> str:  # pragma: no cover
        return "<_DEFAULT_TIMEOUT>"


_DEFAULT_TIMEOUT = _Sentinel()

# Alias type accepted by socket timeouts (float seconds or None)
_TYPE_TIMEOUT = Optional[float]

__all__ = ["_DEFAULT_TIMEOUT", "_TYPE_TIMEOUT"]
