from __future__ import annotations

"""
MAGIC stub: lightweight replacement for a cryptography base module (base_11).

The original module depended on `cryptography.utils` and other internals.
For MAGIC we only need:
- imports to succeed
- a tiny "utils" object with a couple of basic helpers, so type hints or
  simple call sites don't explode.
"""

from typing import Any


class _MagicCryptoUtils:
    """Very small placeholder for cryptography.utils-like helpers."""

    @staticmethod
    def int_to_bytes(value: int) -> bytes:
        # Basic big-endian conversion, enough for tests or simple helpers.
        if value < 0:
            raise ValueError("int_to_bytes stub does not support negative values")
        length = (value.bit_length() + 7) // 8 or 1
        return value.to_bytes(length, "big")

    @staticmethod
    def int_from_bytes(data: bytes) -> int:
        # Inverse of int_to_bytes
        return int.from_bytes(data, "big")


# Public "utils" symbol, so code can do `from cryptography import utils`
# (here mapped to scripts.base_11.utils in the vendored layout).
utils = _MagicCryptoUtils()
