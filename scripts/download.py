"""
MAGIC Week 0 shim for a download helper.

The original module depended on `pip._vendor.requests.models`, which is
tightly coupled to pip's internal layout and not reliable for MAGIC.

For Week 0 smoke tests we only require:
- that importing this module succeeds, and
- that there is a small, side-effect-free API we can call in the future.

No real network I/O happens here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, MutableMapping, Optional


@dataclass
class DownloadResult:
    """
    Tiny stand-in for an HTTP response-like object.

    Week 0: content is always empty, and status_code is 200 by default.
    """
    url: str
    status_code: int = 200
    content: bytes = b""
    headers: MutableMapping[str, str] | None = None


def download_url(url: str, timeout: float = 5.0) -> DownloadResult:
    """
    Dummy download function used in MAGIC smoke tests.

    Parameters
    ----------
    url:
        URL to "download".
    timeout:
        Unused placeholder; kept for API compatibility.

    Returns
    -------
    DownloadResult
        A placeholder object with no real content.
    """
    return DownloadResult(url=url, status_code=200, content=b"", headers={})
