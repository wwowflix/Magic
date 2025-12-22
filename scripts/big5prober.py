from __future__ import annotations

"""
MAGIC shim for scripts.big5prober.

The original module is part of a charset detection suite (Big5 encoding
prober) and depends on state machines, enums, etc.

For MAGIC Week 0 we only need:

- the module to import cleanly
- a simple class that looks like a "prober" with a few attributes/methods
"""

from typing import Optional


class Big5Prober:
    """
    Minimal placeholder for a Big5 charset prober.

    All methods are no-ops, but the surface API is safe to call.
    """

    def __init__(self) -> None:
        self._state: str = "DETECTING"
        self._confidence: float = 0.0

    def reset(self) -> None:
        """Reset internal state (no-op in this shim)."""
        self._state = "DETECTING"
        self._confidence = 0.0

    def feed(self, byte_str: bytes) -> float:
        """
        Inspect incoming bytes and update confidence/state.

        In this MAGIC shim we don't actually analyze data; we just return
        the current confidence (always 0.0).
        """
        return self._confidence

    def get_confidence(self) -> float:
        """Return current confidence value (always 0.0 in this shim)."""
        return self._confidence

    @property
    def charset_name(self) -> Optional[str]:
        """Return the name of the charset this prober targets."""
        return "big5"

    @property
    def state(self) -> str:
        """Return the current internal state as a string."""
        return self._state


__all__ = ["Big5Prober"]
