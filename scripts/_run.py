# ============================================================
# MAGIC RUN CONTEXT HELPER (CLEAN + FIXED VERSION)
# ============================================================

from __future__ import annotations   # MUST BE FIRST

# MAGIC_ASYNCGENS_LAZY_IMPORT
import sys
from typing import TYPE_CHECKING

# ------------------------------------------------------------
# Provide fallback async generator container for safety
# ------------------------------------------------------------
try:
    AsyncGenerators = sys.modules["AsyncGenerators"]  # type: ignore
except Exception:
    class AsyncGenerators:  # minimal no-op to satisfy attrs.Factory
        def __init__(self) -> None:
            pass


# ============================================================
# CORE IMPORT GUARD BLOCK (FIXED INDENTATION)
# ============================================================
try:
    from . import _core  # preferred relative import
except Exception:
    import importlib
    _core = importlib.import_module("scripts._core")
# END MAGIC_RUN_GUARD_BLOCK


# ============================================================
# ENUM + CONTEXT
# ============================================================
import enum


class RunState(enum.Enum):
    INIT = "INIT"
    RUNNING = "RUNNING"
    DONE = "DONE"
    ERROR = "ERROR"


class RunContext:
    """
    Minimal global run context used by generated IO modules.
    """

    def __init__(self) -> None:
        self.state = RunState.INIT
        self.data = {}

    def set_state(self, new_state: RunState) -> None:
        self.state = new_state

    def set(self, key: str, value) -> None:
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)


GLOBAL_RUN_CONTEXT = RunContext()


# Public export
__all__ = ["RunContext", "RunState", "GLOBAL_RUN_CONTEXT"]

# ---- MAGIC compat shim for _NO_SEND (auto-added) ----
try:
    _NO_SEND  # type: ignore[name-defined]
except NameError:  # pragma: no cover - fallback only
    try:
        # Prefer the real anyio implementation if available
        from anyio._core._run import _NO_SEND as _ANYIO_NO_SEND  # type: ignore[import]
    except Exception:  # pragma: no cover
        class _NoSend:
            def __repr__(self) -> str:  # pragma: no cover
                return "<_NO_SEND placeholder>"

        _ANYIO_NO_SEND = _NoSend()
    _NO_SEND = _ANYIO_NO_SEND
# ---- end MAGIC compat shim ----

# ---- MAGIC compat shim for RunStatistics / Task (auto-added) ----
try:
    RunStatistics  # type: ignore[name-defined]
except NameError:  # pragma: no cover - fallback only
    try:
        from anyio._core._run import RunStatistics as _ANYIO_RunStatistics  # type: ignore[import]
        RunStatistics = _ANYIO_RunStatistics  # type: ignore[misc,assignment]
    except Exception:  # pragma: no cover
        from dataclasses import dataclass

        @dataclass
        class RunStatistics:  # type: ignore[override]
            tasks_run: int = 0
            seconds: float = 0.0

try:
    Task  # type: ignore[name-defined]
except NameError:  # pragma: no cover - fallback only
    try:
        from anyio._core._run import Task as _ANYIO_Task  # type: ignore[import]
        Task = _ANYIO_Task  # type: ignore[misc,assignment]
    except Exception:  # pragma: no cover
        class Task:  # type: ignore[override]
            def __init__(self, *args, **kwargs) -> None:
                self.args = args
                self.kwargs = kwargs

            def __repr__(self) -> str:  # pragma: no cover
                return f"<Task placeholder args={self.args!r} kwargs={self.kwargs!r}>"
# ---- end MAGIC compat shim ----

# ---- MAGIC compat shim for RunStatistics / Task (auto-added) ----
try:
    RunStatistics  # type: ignore[name-defined]
except NameError:  # pragma: no cover - define lightweight stand-ins
    from dataclasses import dataclass
    from typing import Any

    @dataclass
    class RunStatistics:
        """Minimal compatibility stub for anyio._core._run.RunStatistics."""
        tasks_started: int = 0
        tasks_finished: int = 0

        def __repr__(self) -> str:  # pragma: no cover
            return (
                f"<RunStatistics started={self.tasks_started} "
                f"finished={self.tasks_finished}>"
            )

    class Task:
        """Minimal compatibility stub for anyio._core._run.Task."""
        def __init__(self, name: str | None = None) -> None:
            self.name = name or "magic-placeholder"

        def __repr__(self) -> str:  # pragma: no cover
            return f"<Task {self.name}>"

# ---- end MAGIC compat shim ----
