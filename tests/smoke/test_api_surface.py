import scripts

def test_scripts_api_surface():
    for name in [
        "StreamError", "StreamClosed", "StreamConsumed",
        "WebSocketError", "WebSocketException",
        "WebSocketProtocolException", "WebSocketConnectionClosedException",
    ]:
        assert hasattr(scripts, name), f"Missing export: {name}"
