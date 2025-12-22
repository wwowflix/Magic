from __future__ import annotations

"""
MAGIC shim for scripts.buffered.

The original module provided buffered byte stream helpers and imported
error types via a parent package:

    from .. import ClosedResourceError, DelimiterNotFound, EndOfStream, IncompleteRead

In MAGIC Week 0 we only need:

- the module to import cleanly
- a few lightweight error classes
- a simple BufferedByteStream-like object

No real async I/O behaviour is required for imports to succeed.
"""

from dataclasses import dataclass, field
from typing import Optional


class ClosedResourceError(RuntimeError):
    """Raised when an operation is attempted on a closed resource."""


class DelimiterNotFound(Exception):
    """Raised when a requested delimiter cannot be found in the stream."""


class EndOfStream(Exception):
    """Raised when the end of the stream is reached."""


class IncompleteRead(Exception):
    """Raised when a read operation cannot read the requested amount of data."""


@dataclass
class BufferedByteStream:
    """
    Minimal stand-in for a buffered byte stream.

    This shim only provides a small subset of behaviour and is primarily meant
    to be safe to construct and call without raising unexpected errors.
    """
    _buffer: bytearray = field(default_factory=bytearray)
    _closed: bool = False

    def write(self, data: bytes) -> None:
        """Append bytes to the internal buffer."""
        if self._closed:
            raise ClosedResourceError("write on closed BufferedByteStream")
        self._buffer.extend(data)

    def read(self, size: Optional[int] = None) -> bytes:
        """
        Read up to *size* bytes from the buffer.

        If size is None, returns the entire buffer.
        """
        if self._closed:
            raise ClosedResourceError("read on closed BufferedByteStream")

        if size is None or size >= len(self._buffer):
            data = bytes(self._buffer)
            self._buffer.clear()
            return data

        data = bytes(self._buffer[:size])
        del self._buffer[:size]
        return data

    def close(self) -> None:
        """Mark the stream as closed."""
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed


__all__ = [
    "ClosedResourceError",
    "DelimiterNotFound",
    "EndOfStream",
    "IncompleteRead",
    "BufferedByteStream",
]
