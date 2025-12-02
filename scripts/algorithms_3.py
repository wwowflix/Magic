"""
MAGIC shim: cryptography algorithms placeholder (ARC4).

The real cryptography.hazmat.decrepit.ciphers.algorithms module is not
available in this environment, so we provide a tiny stand-in that
satisfies imports used in tests/smoke.
"""

from __future__ import annotations


class ARC4:
    """Dummy ARC4 cipher used only for import-time compatibility."""

    def __init__(self, key):
        # store key but do nothing cryptographic
        self._key = bytes(key) if isinstance(key, (bytes, bytearray)) else key

    def encrypt(self, data):
        """Return data unchanged (NO real encryption)."""
        return data

    def decrypt(self, data):
        """Return data unchanged (NO real decryption)."""
        return data


__all__ = ["ARC4"]
