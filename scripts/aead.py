"""MAGIC shim for AEAD crypto primitives.

Provides a tiny AESGCM stand-in so imports succeed without real cryptography
bindings. This is NOT secure and must not be used for real encryption.
"""

from __future__ import annotations

from typing import Any


class AESGCM:
    """Very small no-op stand-in for cryptography.hazmat.primitives.ciphers.aead.AESGCM."""

    def __init__(self, key: bytes) -> None:
        self.key = key

    def encrypt(self, nonce: bytes, data: bytes, associated_data: Any | None = None) -> bytes:
        # Identity transform – for MAGIC import health only.
        return data

    def decrypt(self, nonce: bytes, data: bytes, associated_data: Any | None = None) -> bytes:
        # Identity transform – for MAGIC import health only.
        return data


__all__ = ["AESGCM"]
