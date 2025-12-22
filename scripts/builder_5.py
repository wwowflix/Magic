from __future__ import annotations

"""
MAGIC shim for scripts.builder_5.

The original module pulls in fontTools.otlLib.optimize.gpos and TTFont
GPOS optimization logic.

For MAGIC Week 0 we only need:
- this module to import cleanly
- a harmless "optimizer" API stub that does nothing.
"""

from typing import Any


class GPOSOptimizer:
    """Minimal no-op GPOS optimizer used by MAGIC stubs."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def optimize(self) -> None:
        """No-op optimization."""
        return None


def optimize_gpos(*args: Any, **kwargs: Any) -> None:
    """
    Convenience helper mirroring a typical optimize() / compact() function.
    It simply does nothing and returns None.
    """
    return None


def main(argv: list[str] | None = None) -> int:
    """Optional CLI entry point – does nothing and exits successfully."""
    return 0


__all__ = ["GPOSOptimizer", "optimize_gpos", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
