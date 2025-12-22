from __future__ import annotations

"""
MAGIC shim for scripts.binding (cryptography-style binding).

The original module wraps low-level OpenSSL bindings and imports cryptography.
For MAGIC Week 0 we only need:

- the module to import cleanly
- a Binding class that is safe to construct
- an InternalError exception type for callers to catch
"""


class InternalError(Exception):
    """MAGIC stub for cryptography.exceptions.InternalError."""
    pass


class Binding:
    """
    Minimal stand-in for a cryptography binding object.

    We expose a couple of attributes and classmethods that do nothing but
    keep import-time and light usage safe.
    """

    _initialized: bool = False

    def __init__(self) -> None:
        # In the real implementation these would be FFI / C-lib handles.
        self._ffi = None
        self._lib = None

    @classmethod
    def init_static_locks(cls) -> None:
        """No-op in MAGIC shim; kept for API compatibility."""
        cls._initialized = True

    @classmethod
    def create(cls) -> "Binding":
        """Return a new Binding instance."""
        if not cls._initialized:
            cls.init_static_locks()
        return cls()

    @property
    def ffi(self):
        """Return the FFI handle (always None in this shim)."""
        return self._ffi

    @property
    def lib(self):
        """Return the library handle (always None in this shim)."""
        return self._lib


__all__ = ["Binding", "InternalError"]
