# -*- coding: utf-8 -*-
"""Local 'scripts' package shims for tests."""

class DistlibException(Exception):
    """Local shim to satisfy scripts.resources imports."""
    pass

__all__ = ["DistlibException"]
from .DistlibException import DistlibException
try:  # NBitBase re-export
    from ._nbit import NBitBase  # preferred location
except Exception:  # fallback shim if symbol missing
    class NBitBase:  # type: ignore
        pass
