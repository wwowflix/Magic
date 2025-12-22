from __future__ import annotations

"""
MAGIC stub: lightweight replacement for the cryptography backend module.

The original module imports from `cryptography.hazmat.bindings._rust` and
provides an OpenSSL backend implementation.

For MAGIC we only need:
- safe imports
- a dummy backend object
- get_backend() for call sites that expect it
"""

class DummyBackend:
    """Very small placeholder backend."""

    def __repr__(self):
        return "MAGIC-DummyBackend()"

# module-level backend
BACKEND = DummyBackend()

def get_backend():
    """Return the dummy backend."""
    return BACKEND
