"""
MAGIC Week 0 shim for `cryptography.utils`.

We implement just enough helpers that concatkdf-style code can import and
run basic checks. These are lightweight wrappers around builtins.
"""

from __future__ import annotations

from typing import Any


def int_to_bytes(value: int, length: int) -> bytes:
    """
    Convert integer to big-endian bytes of given length.
    """
    return int(value).to_bytes(length, "big")


def int_from_bytes(data: bytes, byteorder: str = "big", signed: bool = False) -> int:
    """
    Inverse of int.to_bytes. We keep the signature compatible.
    """
    return int.from_bytes(data, byteorder, signed=signed)


def _check_bytes(name: str, value: Any) -> None:
    """
    Minimal type check: ensure value is exactly bytes.
    """
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes-like")


def _check_byteslike(name: str, value: Any) -> None:
    """
    Slightly looser check (like upstream): accept bytes-like objects.
    """
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes-like")


class read_only_property(property):
    """
    Very small stand-in for cryptography.utils.read_only_property.

    We don't need fancy behavior for Week 0; a plain property subclass
    is enough to satisfy imports and attribute access.
    """
    pass


__all__ = [
    "int_to_bytes",
    "int_from_bytes",
    "_check_bytes",
    "_check_byteslike",
    "read_only_property",
]
