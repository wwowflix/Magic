from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import outcome

# MAGIC shim: safely obtain a _core-like object (Trio-style) or a dummy.
try:  # pragma: no cover - best effort
    # Prefer real trio._core if Trio is installed
    import trio._core as _core  # type: ignore[attr-defined]
except Exception:
    class _DummyCore:
        """
        Minimal stand-in for trio._core used in MAGIC smoke tests.

        The tests only import scripts._io_common; they don't rely on
        concrete Trio behavior here, so a dummy object is enough.
        """
        pass

    _core = _DummyCore()


if TYPE_CHECKING:
    from ._io_epoll import EpollWaiters
    from ._io_windows import AFDWaiters


# Utility function shared between _io_epoll and _io_windows
def wake_all(waiters: EpollWaiters | AFDWaiters, exc: BaseException) -> None:
    try:
        current_task = _core.current_task()
    except RuntimeError:
        current_task = None
    raise_at_end = False
    for attr_name in ["read_task", "write_task"]:
        task = getattr(waiters, attr_name)
        if task is not None:
            if task is current_task:
                raise_at_end = True
            else:
                _core.reschedule(task, outcome.Error(copy.copy(exc)))
            setattr(waiters, attr_name, None)
    if raise_at_end:
        raise exc
