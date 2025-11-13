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
