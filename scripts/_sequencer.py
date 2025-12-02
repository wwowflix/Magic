"""MAGIC shim for trio._sequencer."""
from __future__ import annotations

class Sequencer:
    """No-op stand-in used in tests."""
    def __init__(self) -> None:
        self._dummy = True
