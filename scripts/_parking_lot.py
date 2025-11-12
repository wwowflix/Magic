"""
MAGIC-safe shim for scripts._parking_lot.

Provides a minimal global breaker used by run-loop code. No external
imports; safe to import in smoke tests.
"""

from __future__ import annotations


class _Breaker:
    """Tiny event-like breaker."""

    def __init__(self) -> None:
        self._set = False

    def set(self) -> None:
        self._set = True

    def clear(self) -> None:
        self._set = False

    def is_set(self) -> bool:
        return self._set

    # Alias names some callers might use
    trigger = set
    reset = clear


# Exported singleton expected by scripts._run and friends
GLOBAL_PARKING_LOT_BREAKER = _Breaker()

__all__ = ["GLOBAL_PARKING_LOT_BREAKER"]
