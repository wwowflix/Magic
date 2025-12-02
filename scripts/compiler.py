from __future__ import annotations

"""
Week 0 stub for `scripts.compiler`.

The original module depends on `altair.utils.PluginRegistry` to manage
compilers for chart rendering. For MAGIC Week 0 smoke-import tests we only
need this module to import cleanly; no real Altair integration is required.
"""

from typing import Any, Callable, Dict, Optional


class PluginRegistry:
    """
    Minimal stand-in for altair.utils.PluginRegistry.

    It stores callables by name and lets callers retrieve them later.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._plugins[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        return self._plugins.get(name, self._noop)

    def names(self):
        return list(self._plugins.keys())

    def _noop(self, *args: Any, **kwargs: Any) -> None:
        return None


# Global registry instance (similar to the real module pattern).
COMPILERS = PluginRegistry()


def enable(name: str, func: Optional[Callable[..., Any]] = None) -> None:
    """
    Register a compiler under the given name in the Week 0 stub.

    If func is None, this is a no-op.
    """
    if func is not None:
        COMPILERS.register(name, func)
