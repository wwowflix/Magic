"""MAGIC shim for pytest-style testing helpers.

The original module contained complex plugin code; here we only define
a very small placeholder so imports succeed.
"""

from __future__ import annotations


class DummyTestHelper:
    """No-op helper placeholder used only for imports."""
    pass

# ---- MAGIC TaskInfo shim (do not remove) ----
try:
    from dataclasses import dataclass
except Exception:  # very defensive, but never break imports
    def dataclass(cls):
        return cls

@dataclass
class TaskInfo:  # minimal stub for MAGIC imports
    """
    Minimal MAGIC shim for async TaskInfo.

    Only needs to be importable; tests do not rely on real fields.
    """
    id: object | None = None
    name: str | None = None
    state: str | None = None

def get_current_task(*args, **kwargs):
    """
    MAGIC shim for async get_current_task.

    Returns a dummy TaskInfo so that callers have something truthy,
    but we avoid any real async framework dependency.
    """
    return TaskInfo(id=None, name="MAGIC-shim-task", state="unknown")
# ---- END MAGIC TaskInfo shim ----
