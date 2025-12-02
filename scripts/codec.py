from __future__ import annotations

"""
Week 0 stub for `scripts.codec`.

The original module is typically part of an IDNA codec implementation
and imports `encode`, `decode`, `alabel`, `ulabel`, and `IDNAError`
from a `core` module. For MAGIC Week 0, we only need this module to
import cleanly, so we provide minimal stand-ins here without depending
on `scripts.core`.
"""

from typing import Tuple, Any


class IDNAError(UnicodeError):
    """Minimal stand-in exception type for IDNA-related errors."""
    pass


def encode(input: Any, errors: str = "strict") -> Tuple[bytes, int]:
    """
    Very simple stub: encode text as ASCII bytes.

    This is NOT a full IDNA implementation. It only exists so that
    vendored code can call `codec.encode` without crashing.
    """
    text = str(input)
    data = text.encode("ascii", errors=errors)
    return data, len(text)


def decode(input: Any, errors: str = "strict") -> Tuple[str, int]:
    """
    Very simple stub: decode ASCII bytes back to text.
    """
    if isinstance(input, str):
        # Already text
        return input, len(input)
    data = bytes(input)
    text = data.decode("ascii", errors=errors)
    return text, len(data)


def alabel(label: Any) -> bytes:
    """
    Stub for converting a Unicode label to an ASCII label.
    Here we simply ASCII-encode the string form of the label.
    """
    return str(label).encode("ascii", errors="strict")


def ulabel(label: Any) -> str:
    """
    Stub for converting an ASCII label to Unicode.
    Here we simply decode as ASCII if bytes, or str() otherwise.
    """
    if isinstance(label, bytes):
        return label.decode("ascii", errors="strict")
    return str(label)
