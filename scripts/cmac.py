from __future__ import annotations

"""
Week 0 stub for scripts.cmac.

The original module is from the cryptography package and depends on
cryptography.hazmat.bindings._rust. For smoke-import tests in MAGIC
we only need a minimal CMAC-like object that can be imported without
the real cryptography backend.
"""

from typing import Any


class CMAC:
    """
    Minimal CMAC-like object.

    This implementation does NOT provide real cryptographic security and
    must not be used in production. It is only present so that vendored
    sample code and tests can import scripts.cmac during Week 0.
    """

    def __init__(self, key: bytes, algorithm: Any | None = None, backend: Any | None = None) -> None:
        self._key = key
        self._algorithm = algorithm
        self._backend = backend
        self._buffer = b""

    def update(self, data: bytes) -> None:
        """
        Append data to the internal buffer.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes-like")
        self._buffer += bytes(data)

    def finalize(self) -> bytes:
        """
        Return a deterministic but NON-SECURE tag.

        For now this just returns 16 zero bytes. Real CMAC logic can be
        implemented in a later Week if needed.
        """
        return b"\x00" * 16

    def copy(self) -> "CMAC":
        """
        Return a shallow copy of this CMAC object.
        """
        clone = CMAC(self._key, self._algorithm, self._backend)
        clone._buffer = self._buffer
        return clone

    def verify(self, tag: bytes) -> None:
        """
        Verify a tag produced by inalize.

        In this stub, we simply compare bytes and raise ValueError on mismatch.
        """
        if self.finalize() != tag:
            raise ValueError("CMAC tag does not match (stub implementation)")
