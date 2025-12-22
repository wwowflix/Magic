from __future__ import annotations

"""
MAGIC – Week 0 compression shim.

Goal
----
- Allow `import scripts.compression` to succeed during global smoke tests.
- Avoid importing heavy / missing dependencies like `fsspec`.
- Provide minimal, safe placeholder helpers that can be replaced later.

The original vendored module has been moved to:
    compression.py.magic_bak_week0
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CompressionResult:
    """Tiny result object describing a pretend compression run."""
    raw_size: int
    compressed_size: int
    algorithm: str = "none"


def compress_bytes(data: bytes, algorithm: str = "none") -> CompressionResult:
    """
    Week 0 placeholder: pretend to "compress" data.

    For now we:
    - Do NOT actually compress.
    - Just report sizes and echo the algorithm name.
    """
    size = len(data)
    return CompressionResult(raw_size=size, compressed_size=size, algorithm=algorithm)


def decompress_bytes(data: bytes, algorithm: str = "none") -> bytes:
    """
    Week 0 placeholder: identity transform.

    Any caller that uses this in Week 0 will just get its bytes back.
    """
    return data


__all__ = ["CompressionResult", "compress_bytes", "decompress_bytes"]
