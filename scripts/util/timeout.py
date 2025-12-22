from __future__ import annotations

"""
MAGIC – Week 0 util.timeout shim.

Goal
----
- Provide the minimal symbols expected by:
    - scripts._base_connection
    - scripts.connectionpool
- Avoid pulling in the real urllib3 implementation.
- Safe, no-network, no-real-timeouts behaviour for Week 0.
"""

from typing import Any, Optional


# Sentinel used by urllib3 as "use default timeout".
# Here it's just a unique object.
class _DefaultTimeoutSentinel:
    pass


_DEFAULT_TIMEOUT = _DefaultTimeoutSentinel()

# Runtime type aliases – in real urllib3 this is a union of:
#   - Timeout
#   - int / float / None
#   - the default sentinel
# For Week 0 we only need the names to exist.
_TYPE_DEFAULT = Any
_TYPE_TIMEOUT = Any  # extra alias used by scripts._base_connection


class Timeout:
    """
    Minimal Week 0 Timeout object.

    We store the usual attributes (total, connect, read) so code that
    inspects them won't explode, but all logic is very relaxed.
    """

    def __init__(
        self,
        total: Any = _DEFAULT_TIMEOUT,
        connect: Any = _DEFAULT_TIMEOUT,
        read: Any = _DEFAULT_TIMEOUT,
    ) -> None:
        self.total = total
        self.connect = connect
        self.read = read

    # ---- class helpers -------------------------------------------------

    @classmethod
    def _validate_timeout(cls, value: Any) -> Any:
        """
        Week 0: accept any value and return it unchanged.
        """
        return value

    @classmethod
    def from_float(cls, timeout: Optional[float]) -> "Timeout":
        """
        Week 0 convenience: create a Timeout with total=timeout.
        """
        return cls(total=timeout)

    # ---- instance helpers ----------------------------------------------

    def clone(self) -> "Timeout":
        """
        Return a shallow copy of this Timeout.
        """
        return Timeout(self.total, self.connect, self.read)

    def start_connect(self) -> None:
        """
        Week 0 no-op hook called before a connection attempt.
        """
        return None

    def get_connect_duration(self) -> Optional[float]:
        """
        Week 0: we don't track durations, so always return None.
        """
        return None

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Timeout(total={self.total!r}, "
            f"connect={self.connect!r}, read={self.read!r})"
        )


__all__ = ["_DEFAULT_TIMEOUT", "_TYPE_DEFAULT", "_TYPE_TIMEOUT", "Timeout"]
