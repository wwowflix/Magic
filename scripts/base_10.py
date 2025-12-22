from __future__ import annotations

"""
MAGIC stub: lightweight replacement for a cryptography backend variant.

The original base_10 module imported from
`cryptography.hazmat.bindings._rust` and provided an OpenSSL backend.

For MAGIC we only need:
- safe imports
- a dummy backend object
- get_backend() for call sites that expect it
"""

try:
    # If our main backend shim exists, reuse it so behavior is consistent.
    from .backend import BACKEND as BACKEND, get_backend as get_backend  # type: ignore[attr-defined]
except Exception:
    # Fallback: define a local dummy backend.
    class DummyBackend:
        """Very small placeholder backend."""

        def __repr__(self) -> str:  # pragma: no cover
            return "MAGIC-DummyBackend(base_10)"

    BACKEND = DummyBackend()

    def get_backend():
        """Return the dummy backend."""
        return BACKEND
