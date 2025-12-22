from __future__ import annotations

"""
MAGIC stub: lightweight replacement for a cryptography base module (base_9).

The original file imported from `cryptography.hazmat.bindings._rust` and
provided OpenSSL-related helpers.

For MAGIC Week 0 we only need:
- imports to succeed
- an object that looks like a "backend" so any light usage does not explode.
"""


class DummyCryptoBackend:
    """Very small placeholder backend used by MAGIC stubs."""

    def __repr__(self) -> str:  # pragma: no cover
        return "MAGIC-DummyCryptoBackend()"

    # You can add small helpers here later if some call sites need them.
    # For imports and basic repr, this is already enough.


# Public symbol commonly expected from cryptography backends
BACKEND = DummyCryptoBackend()


def get_backend() -> DummyCryptoBackend:
    """
    Return the dummy backend.

    This mirrors the shape of typical cryptography "get_backend" helpers.
    """
    return BACKEND
