from __future__ import annotations

"""
MAGIC – Week 0 concat KDF shim.

Goal
----
- Allow `import scripts.concatkdf` to succeed during global smoke tests.
- Avoid depending on the `cryptography` package.
- Provide a tiny, deterministic KDF-like class that is "good enough" for tests
  that may instantiate it.

The original vendored module has been moved to:
    concatkdf.py.magic_bak_week0

A later week can reintroduce a proper adapter using `cryptography`.
"""

from dataclasses import dataclass
from typing import Optional, Union


BytesLike = Union[bytes, bytearray]


@dataclass
class ConcatKDFHash:
    """
    Extremely simplified, non-cryptographic stand-in for a Concat KDF.

    WARNING: This is **not** secure and is only intended for Week 0 imports.
    It just repeats the input key material until the requested length.
    """
    algorithm: str = "SHA256"
    length: int = 32
    otherinfo: Optional[bytes] = None

    def derive(self, key_material: BytesLike) -> bytes:
        if not isinstance(key_material, (bytes, bytearray)):
            key_material = bytes(str(key_material), "utf-8")

        if not key_material:
            key_material = b"\x00"

        # Repeat the bytes until we reach the target length, then truncate.
        repeated = (key_material * ((self.length // len(key_material)) + 1))[: self.length]
        return bytes(repeated)

    def verify(self, key_material: BytesLike, expected_key: bytes) -> None:
        """
        Minimal verify helper: recompute and compare bytes.
        Raises ValueError if mismatch.
        """
        if self.derive(key_material) != expected_key:
            raise ValueError("ConcatKDFHash.verify() failed (Week 0 stub)")


__all__ = ["ConcatKDFHash"]
