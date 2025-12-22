from __future__ import annotations

"""
MAGIC stub implementation for the kqueue-based I/O backend.

On platforms that do not expose ``select.kqueue`` (like Windows),
this module only exists so that imports succeed:

    import scripts._io_kqueue

The real Trio implementation only runs on BSD-style systems.
Here we provide a minimal stub that makes the smoke tests happy
(import works, symbol exists) without actually doing anything.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # type hints only, no heavy imports at runtime
    from typing import Any


class KqueueIOManager:
    """
    Stub KqueueIOManager used in MAGIC on non-kqueue platforms.

    Any attempt to instantiate this class will raise a clear error.
    Its purpose is only to satisfy imports in tests such as
    ``test_smoke_scripts__io_kqueue.py``.
    """

    def __init__(self, *args: "Any", **kwargs: "Any") -> None:  # pragma: no cover
        raise RuntimeError(
            "KqueueIOManager is not available on this platform "
            "(select.kqueue is missing)."
        )


__all__ = ["KqueueIOManager"]
