"""
MAGIC-safe shim for scripts._generated_instrumentation.

The original module wires runtime instrumentation into an async run loop.
For MAGIC we do NOT need real instrumentation; we only need this module
to be safe to import during smoke tests.

This shim provides a minimal, side-effect free API surface.
"""

from __future__ import annotations
from typing import Any


class GeneratedInstrumentation:
    """No-op instrumentation placeholder.

    Methods accept arbitrary arguments and do nothing. This keeps the
    surface area stable for any callers that just expect a .instrument()
    method or similar.
    """

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = bool(enabled)

    def instrument(self, *args: Any, **kwargs: Any) -> None:
        """Pretend to instrument something, but do nothing."""
        return None

    def __repr__(self) -> str:  # pragma: no cover - trivial repr
        return f"{self.__class__.__name__}(enabled={self.enabled!r})"


# A default singleton instance that callers can reuse.
DEFAULT_INSTRUMENTATION = GeneratedInstrumentation(enabled=False)

__all__ = ["GeneratedInstrumentation", "DEFAULT_INSTRUMENTATION"]
