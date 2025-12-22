from __future__ import annotations

"""
MAGIC – Week 0 util.ssl_match_hostname shim.

Goal
----
- Provide a minimal CertificateError and match_hostname so that
  scripts.connectionpool imports cleanly.
- Prefer to delegate to stdlib ssl.match_hostname when available.
"""

from typing import Any
import ssl as _ssl


class CertificateError(ValueError):
    """Week 0 stand-in for urllib3.util.ssl_match_hostname.CertificateError."""
    pass


def match_hostname(cert: Any, hostname: str) -> None:
    """
    Week 0 wrapper around stdlib ssl.match_hostname (if present).

    Parameters
    ----------
    cert : Any
        Certificate dict/structure (ignored by this shim if ssl.match_hostname
        is not available).
    hostname : str
        Target hostname.
    """
    try:
        fn = getattr(_ssl, "match_hostname", None)
    except Exception:
        fn = None

    if fn is not None:
        # Use the real stdlib implementation when possible
        return fn(cert, hostname)  # type: ignore[call-arg]

    # Fallback: assume OK, do nothing.
    return None


__all__ = ["CertificateError", "match_hostname"]
