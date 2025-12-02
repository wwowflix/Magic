from __future__ import annotations

"""
MAGIC – Week 0 util.request shim.

Goal
----
- Provide the minimal runtime symbols expected by:
    - scripts.connectionpool
- Avoid pulling in the real urllib3 implementation.

We only define:
- _TYPE_BODY_POSITION  – a loose type alias.
- set_file_position()  – a best-effort, no-throw helper.
"""

from typing import Any, Optional

# In real urllib3 this is a more specific type. For Week 0 we just need
# the symbol to exist and behave reasonably.
_TYPE_BODY_POSITION = Optional[int]


def set_file_position(body: Any, body_pos: _TYPE_BODY_POSITION) -> _TYPE_BODY_POSITION:
    """
    Week 0 stub: best-effort rewind for file-like bodies, otherwise no-op.

    Parameters
    ----------
    body : Any
        Request body object; may be a file-like object with .seek().
    body_pos : Optional[int]
        Previously recorded position; if provided, we try to seek back.

    Returns
    -------
    Optional[int]
        The (possibly unchanged) body_pos so callers can keep tracking it.
    """
    if body is not None and body_pos is not None:
        try:
            if hasattr(body, "seek"):
                body.seek(body_pos)
        except Exception:
            # Never let this break import-time logic in Week 0.
            pass
    return body_pos


__all__ = ["_TYPE_BODY_POSITION", "set_file_position"]
