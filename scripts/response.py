"""MAGIC shim for urllib3-style response helpers.

We just expose a minimal BaseHTTPResponse so that imports succeed.
"""

from __future__ import annotations


class BaseHTTPResponse:  # type: ignore[override]
    """Minimal stand-in used only for MAGIC tests."""
    pass
