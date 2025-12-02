from __future__ import annotations

"""
MAGIC shim for trio-style Windows pipe streams.

This is a minimal, import-only stub. It intentionally avoids any
real Windows API usage. Smoke tests only need this module to import.
"""

from typing import Any

try:
    from ._abc import ReceiveStream, SendStream  # type: ignore
except Exception:  # extremely defensive: never break imports
    class ReceiveStream:  # type: ignore[override]
        """Fallback stub base class for receive streams."""
        pass

    class SendStream:  # type: ignore[override]
        """Fallback stub base class for send streams."""
        pass


class PipeSendStream(SendStream):
    """Trivial stub representing a write-end of a pipe."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed = False

    def close(self) -> None:
        self._closed = True


class PipeReceiveStream(ReceiveStream):
    """Trivial stub representing a read-end of a pipe."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._closed = False

    def close(self) -> None:
        self._closed = True
