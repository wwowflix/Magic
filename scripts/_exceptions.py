# -*- coding: utf-8 -*-
"""Exception shims for scripts package (MAGIC Week 6 Step 6.2)."""

__all__ = [
    "StreamError", "StreamClosed", "StreamConsumed",
    "WebSocketError", "WebSocketException",
    "WebSocketProtocolException", "WebSocketConnectionClosedException",
    "WebSocketBadStatusException", "WebSocketAddressException", "WebSocketTimeoutException","WebSocketProxyException"]

# Base classes
class StreamError(Exception):
    """Base class for stream-related errors."""
    pass

class WebSocketError(Exception):
    """Base class for WebSocket-related errors."""
    pass

# Backwards-compat alias some stacks expect
WebSocketException = WebSocketError

# Stream exceptions used by scripts._content
class StreamClosed(StreamError):
    """Operation attempted on a closed stream."""
    pass

class StreamConsumed(StreamError):
    """Stream has already been consumed."""
    pass

# WebSocket exceptions used by scripts._core / scripts._app / _handshake
class WebSocketProtocolException(WebSocketError):
    """Protocol error in WebSocket handshake/frames."""
    pass

class WebSocketConnectionClosedException(WebSocketError):
    """Operation attempted on a closed WebSocket connection."""
    pass

class WebSocketBadStatusException(WebSocketException):
    """Server returned an unexpected HTTP status during WebSocket handshake."""
    def __init__(self, status_code: int, msg: str | None = None):
        self.status_code = status_code
        super().__init__(msg or f"Bad status code: {status_code}")

class WebSocketAddressException(WebSocketException):
    """Failed to resolve or connect to WebSocket host/port."""
    pass

class WebSocketTimeoutException(WebSocketException):
    """Operation timed out during WebSocket handshake or IO."""
    pass

class WebSocketProxyException(WebSocketException):
    'WebSocket proxy configuration or negotiation error.'
    pass
