"""
MAGIC Week 0: safe stub for plugin_registry.

Goal:
- Allow "import scripts.plugin_registry" and "PluginRegistry[...]" to succeed.
- Avoid importing altair, pandas, or any heavy plugin machinery.
- Provide a minimal PluginRegistry with register/get/all.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Generic, TypeVar

TFunc = TypeVar("TFunc", bound=Callable[..., Any])
TReturn_co = TypeVar("TReturn_co", covariant=True)


class PluginRegistry(Generic[TFunc, TReturn_co]):
    """
    Minimal Week-0 plugin registry placeholder.

    The Generic[...] typing is for type-checkers only.
    At runtime, type arguments are ignored via __class_getitem__,
    so PluginRegistry[DataTransformerType, R] works without error.
    """

    def __init__(self) -> None:
        self._store: Dict[str, TFunc] = {}

    def __class_getitem__(cls, item: object) -> "PluginRegistry[TFunc, TReturn_co]":  # type: ignore[type-arg]
        # Allow PluginRegistry[...] syntax but ignore the concrete types.
        return cls

    def register(self, name: str, func: TFunc) -> None:
        self._store[name] = func

    def get(self, name: str) -> TFunc | None:
        return self._store.get(name)

    def all(self) -> Dict[str, TFunc]:
        return dict(self._store)


# Global instance (expected by data.py)
plugin_registry: PluginRegistry[Any, Any] = PluginRegistry()

__all__ = ["PluginRegistry", "plugin_registry"]
