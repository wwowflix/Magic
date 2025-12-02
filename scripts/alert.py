"""MAGIC stub for selenium-based Alert.

The real implementation depends on selenium; this stub only keeps the API
surface needed for imports in MAGIC tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Alert:
    """Minimal Alert stand-in."""

    text: str = ""

    def accept(self) -> None:  # pragma: no cover - side-effect free
        """Pretend to accept the alert."""
        return None

    def dismiss(self) -> None:  # pragma: no cover
        """Pretend to dismiss the alert."""
        return None

    def send_keys(self, *keys: Any) -> None:  # pragma: no cover
        """Pretend to type into the alert."""
        return None


__all__ = ["Alert"]
