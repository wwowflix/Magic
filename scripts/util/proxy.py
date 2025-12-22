from __future__ import annotations

"""
MAGIC – Week 0 util.proxy shim.

Goal
----
- Provide the minimal runtime symbol expected by:
    - scripts.connectionpool
- Avoid pulling in the real urllib3 implementation or doing any
  real proxy / tunnelling logic.
"""

from typing import Any


def connection_requires_http_tunnel(*args: Any, **kwargs: Any) -> bool:
    """
    Week 0 stub: always report that an HTTP tunnel is NOT required.

    Parameters
    ----------
    *args, **kwargs
        Kept for future compatibility with urllib3-style callers.

    Returns
    -------
    bool
        Always False for Week 0 – safe default for smoke tests.
    """
    return False


__all__ = ["connection_requires_http_tunnel"]
