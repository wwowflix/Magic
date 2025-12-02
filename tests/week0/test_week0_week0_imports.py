"""
MAGIC - Week 0 Verification Tests

These tests only check the parts of Week 0 that are code-verifiable:

- W0-1: Extended WebSocket Shim exists and imports
- W0-1.*: DEFAULT_SOCKET_OPTION, recv_line, send_bytes exist
- W0-2: WebSocket/HTTP smokes don't immediately explode on import level

Non-code tasks (Notion update, git tagging, docs) are NOT validated here.
"""

import importlib


def _import_socket_http_extended():
    """Helper to import the extended socket shim."""
    return importlib.import_module("scripts._socket_http_extended")


def test_w0_1_socket_http_extended_imports():
    """
    W0-1: Implement Extended WebSocket Shim

    Pass criteria:
    - scripts._socket_http_extended imports without ImportError/SyntaxError
    """
    mod = _import_socket_http_extended()
    assert mod is not None


def test_w0_1_symbols_present():
    """
    W0-1.*: Required symbols exist on the shim module

    Pass criteria:
    - DEFAULT_SOCKET_OPTION exists
    - recv_line callable exists
    - send_bytes callable exists
    """
    mod = _import_socket_http_extended()

    assert hasattr(mod, "DEFAULT_SOCKET_OPTION"), "DEFAULT_SOCKET_OPTION missing"
    assert hasattr(mod, "recv_line"), "recv_line() missing"
    assert hasattr(mod, "send_bytes"), "send_bytes() missing"

    assert callable(mod.recv_line), "recv_line is not callable"
    assert callable(mod.send_bytes), "send_bytes is not callable"


def test_w0_2_http_socket_import_sanity():
    """
    W0-2: WebSocket + HTTP smokes (import-level sanity only)

    We only test that these modules can import without exploding.
    """
    candidates = [
        "scripts._socket_http_extended",  # core shim
        # Add more related modules here later if needed:
        # "scripts._websocket_client_compat",
        # "scripts._http_wrappers",
    ]

    for name in candidates:
        mod = importlib.import_module(name)
        assert mod is not None, f"Import failed for {name}"
