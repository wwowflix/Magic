"""
MAGIC Week 0: ultra-minimal util.connection shim.

Goal:
- Let "from scripts.util import connection" work.
- Provide _TYPE_SOCKET_OPTIONS so scripts._base_connection can import it.
- Provide is_connection_dropped for connectionpool.
- No real network I/O; everything is safe and fake for Week 0.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional

# Type alias used by scripts._base_connection
_TYPE_SOCKET_OPTIONS = Optional[Mapping[str, Any]]


def is_connection_dropped(conn: Any) -> bool:
    """
    Week 0 stub for urllib3.util.connection.is_connection_dropped.

    Parameters
    ----------
    conn : Any
        Connection object (ignored in this stub).

    Returns
    -------
    bool
        Always False for Week 0 – we pretend the connection is not dropped.
    """
    try:
        _ = getattr(conn, "closed", None)  # touch attribute for debugging only
    except Exception:
        pass
    return False


__all__ = ["_TYPE_SOCKET_OPTIONS", "is_connection_dropped"]
