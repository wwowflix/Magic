class StreamError(Exception):
    """Base class for stream-related errors."""
    pass


class WebSocketError(Exception):
    """Base class for WebSocket-related errors."""
    pass


# Backwards-compat alias
WebSocketException = WebSocketError


class StreamClosed(StreamError):
    """Operation attempted on a closed stream."""
    pass


class StreamConsumed(StreamError):
    """Stream has already been consumed."""
    pass


class WebSocketProtocolException(WebSocketError):
    """Protocol error in WebSocket handshake/frames."""
    pass


class WebSocketConnectionClosedException(WebSocketError):
    """Operation attempted on a closed WebSocket connection."""
    pass
