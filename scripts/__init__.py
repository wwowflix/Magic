"""
MAGIC scripts package.

This module exposes a stable public API surface used by tests/smoke,
including a few compatibility shims so that external code can rely on
these names even if underlying libraries or versions change.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Compatibility shims for stream / websocket errors
# ---------------------------------------------------------------------------
# The smoke test tests/smoke/test_api_surface.py expects these names to be
# available directly on the `scripts` package:
#
#   StreamError
#   StreamClosed
#   StreamConsumed
#   WebSocketError
#   WebSocketException
#   WebSocketProtocolException
#   WebSocketConnectionClosedException
#
# We try to reuse real library types when available, and fall back to
# local placeholder classes otherwise. The tests only care that the
# attributes exist – type details are not important for now.
# ---------------------------------------------------------------------------

# --- HTTP stream errors (prefer httpx if present) ---------------------------

try:
    # httpx >= 0.18 exposes these error types
    from httpx import StreamError as _RealStreamError  # type: ignore
    from httpx import StreamClosed as _RealStreamClosed  # type: ignore
    from httpx import StreamConsumed as _RealStreamConsumed  # type: ignore
except Exception:  # pragma: no cover - defensive fallback

    class _RealStreamError(Exception):
        """Compatibility placeholder for httpx.StreamError."""

    class _RealStreamClosed(_RealStreamError):
        """Compatibility placeholder for httpx.StreamClosed."""

    class _RealStreamConsumed(_RealStreamError):
        """Compatibility placeholder for httpx.StreamConsumed."""


StreamError = _RealStreamError
StreamClosed = _RealStreamClosed
StreamConsumed = _RealStreamConsumed

# --- WebSocket errors (prefer websocket-client if present) ------------------

try:
    from websocket import (  # type: ignore
        WebSocketException as _WSException,
        WebSocketProtocolException as _WSProtocolException,
        WebSocketConnectionClosedException as _WSConnectionClosedException,
    )

    # Some ecosystems distinguish WebSocketError, some don’t:
    WebSocketError = _WSException
    WebSocketException = _WSException
    WebSocketProtocolException = _WSProtocolException
    WebSocketConnectionClosedException = _WSConnectionClosedException

except Exception:  # pragma: no cover - defensive fallback

    class WebSocketError(Exception):
        """Base compatibility websocket error."""

    class WebSocketException(WebSocketError):
        """Generic websocket exception."""

    class WebSocketProtocolException(WebSocketException):
        """Protocol-level websocket error."""

    class WebSocketConnectionClosedException(WebSocketException):
        """Raised when websocket connection is already closed."""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "StreamError",
    "StreamClosed",
    "StreamConsumed",
    "WebSocketError",
    "WebSocketException",
    "WebSocketProtocolException",
    "WebSocketConnectionClosedException",
]
