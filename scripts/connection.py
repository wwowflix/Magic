from __future__ import annotations

"""
MAGIC – Week 0 connection shim.

Goal
----
- Provide the symbols that scripts.connectionpool imports:
  BaseSSLError, BrokenPipeError, DummyConnection, HTTPConnection,
  HTTPException, HTTPSConnection, ProxyConfig, _wrap_proxy_error,
  port_by_scheme.
- No real network logic – purely for import-time safety.
"""

from typing import Any, Dict


class BaseSSLError(Exception):
    """Week 0 placeholder for SSL-related errors."""


class HTTPException(Exception):
    """Generic HTTP error placeholder."""


class BrokenPipeError(IOError):
    """Broken pipe placeholder."""


class DummyConnection:
    """No-op connection used for Week 0."""

    def close(self) -> None:  # pragma: no cover
        pass


class HTTPConnection:
    def __init__(self, host: str = "", port: int | None = None, *args: Any, **kwargs: Any) -> None:
        self.host = host
        self.port = port
        self.args = args
        self.kwargs = kwargs

    def close(self) -> None:  # pragma: no cover
        pass


class HTTPSConnection(HTTPConnection):
    """HTTPS variant of HTTPConnection (no behavioural differences for Week 0)."""


class ProxyConfig:
    """
    Very small Week 0 proxy config stub.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ProxyConfig {self.kwargs!r}>"


def _wrap_proxy_error(exc: Exception) -> Exception:
    """
    Week 0 helper: simply return the original exception.
    """
    return exc


# Minimal port map – enough for import-time use.
port_by_scheme: Dict[str, int] = {
    "http": 80,
    "https": 443,
}

__all__ = [
    "BaseSSLError",
    "BrokenPipeError",
    "DummyConnection",
    "HTTPConnection",
    "HTTPException",
    "HTTPSConnection",
    "ProxyConfig",
    "_wrap_proxy_error",
    "port_by_scheme",
]
