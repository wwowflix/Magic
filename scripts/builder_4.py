from __future__ import annotations

"""
MAGIC shim for scripts.builder_4.

The original module uses fontTools.feaLib.parser and varLib builder, which
pull in advanced OpenType variation logic.

For MAGIC Week 0 we only need:
- the module to import cleanly
- a tiny "builder" API that does nothing but doesn’t crash
"""

from typing import Any


class FeatureBuilder:
    """
    Minimal placeholder builder used in MAGIC.

    Accepts any args/kwargs, exposes a .build() method that is a no-op.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def build(self) -> None:
        """No-op build method."""
        return None


def build_features(*args: Any, **kwargs: Any) -> None:
    """
    Convenience no-op helper to mirror a typical 'build' function.
    """
    return None


def main(argv: list[str] | None = None) -> int:
    """
    Optional CLI entry point that does nothing and exits successfully.
    """
    return 0


__all__ = ["FeatureBuilder", "build_features", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
