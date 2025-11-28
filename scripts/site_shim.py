from __future__ import annotations

"""
MAGIC Week 0 – Narrow third-party import shim.

Only intercepts imports for:
    - pip.*
    - cmdstanpy.*

Everything else (pandas, numpy, etc.) is left alone to avoid weird
runtime behaviour and crashes in pytest.
"""

import importlib.machinery
import sys
import types
from typing import Any, Tuple


THIRDPARTY_PREFIXES: Tuple[str, ...] = (
    "pip",
    "cmdstanpy",
)


class MagicAttr:
    """Simple dummy attribute object that is safe to repr and call."""

    def __init__(self, name: str) -> None:
        self.__name__ = name

    def __repr__(self) -> str:
        return f"<MagicAttr {self.__name__}>"

    def __call__(self, *args: Any, **kwargs: Any) -> "MagicAttr":
        return self


class MagicDummy(types.ModuleType):
    """
    Dummy module which happily absorbs any attribute access.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def __getattr__(self, item: str) -> Any:
        attr = MagicAttr(f"{self.__name__}.{item}")
        setattr(self, item, attr)
        return attr

    def __repr__(self) -> str:
        return f"<MagicDummyModule {self.__name__}>"


class StubLoader(importlib.machinery.SourceFileLoader):
    """
    Loader that simply creates an empty MagicDummy module.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name, "<magic-stub>")

    def create_module(self, spec):
        return MagicDummy(spec.name)

    def exec_module(self, module) -> None:
        # Nothing to execute for stub modules.
        return


class StubFinder:
    """
    Meta path finder that intercepts imports for well-known third-party
    prefixes and returns a stub module instead of failing.
    """

    def find_spec(self, fullname: str, path, target=None):
        # If we already have a real module, leave it alone.
        if fullname in sys.modules:
            return None

        # Only handle specific third-party prefixes.
        if not fullname.startswith(THIRDPARTY_PREFIXES):
            return None

        loader = StubLoader(fullname)
        return importlib.machinery.ModuleSpec(fullname, loader)


def install_thirdparty_shims() -> None:
    """
    Install the StubFinder once at the front of sys.meta_path.
    """
    for finder in sys.meta_path:
        if isinstance(finder, StubFinder):
            return
    sys.meta_path.insert(0, StubFinder())
