"""
MAGIC-safe shim for scripts._exceptions.

Provides minimal exception types required by other scripts modules:

- Cancelled
- RunFinishedError
- TrioInternalError
- WebSocketProtocolException
- WebSocketConnectionClosedException
- WebSocketException
- WebSocketBadStatusException

These are intentionally simple and side-effect free. They exist so that
imports from scripts._run, scripts._core, scripts._handshake, and related
modules succeed during MAGIC tests.
"""

from __future__ import annotations


class TrioInternalError(Exception):
    """Internal error in the runtime."""


class RunFinishedError(Exception):
    """Raised when an operation is attempted on a finished run loop."""


class WebSocketProtocolException(Exception):
    """Generic WebSocket protocol error placeholder."""


class WebSocketConnectionClosedException(Exception):
    """Raised when a WebSocket connection is already closed."""


class WebSocketException(Exception):
    """Base WebSocket exception placeholder."""


class WebSocketBadStatusException(WebSocketException):
    """Raised when an HTTP handshake returns an unacceptable status code."""


class Cancelled(BaseException):
    """Cancellation signal placeholder."""
    pass


__all__ = [
    "Cancelled",
    "RunFinishedError",
    "TrioInternalError",
    "WebSocketProtocolException",
    "WebSocketConnectionClosedException",
    "WebSocketException",
    "WebSocketBadStatusException",
]
