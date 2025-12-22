from __future__ import annotations

"""
MAGIC shim for scripts.socket

- Thin wrapper around the stdlib `socket` module.
- Used by scripts._highlevel_open_tcp_listeners as `tsocket`.
- Does NOT touch sys.modules["_socket"] or the built-in C extension.
"""

import socket as _stdlib_socket
from socket import *  # re-export all public names from stdlib socket

# Explicit alias so callers can do `tsocket.socket(...)`
socket = _stdlib_socket

# Keep a clean, explicit export list
__all__ = [name for name in dir(_stdlib_socket) if not name.startswith("_")]
