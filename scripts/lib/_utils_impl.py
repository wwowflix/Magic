from __future__ import annotations

# --- MAGIC lib utils shim ---
from pathlib import Path


def get_include() -> str:
    """
    Minimal compat: return a usable include directory.
    Many projects use this to locate headers; we return
    the package dir so callers can resolve relative paths.
    """
    return str(Path(__file__).resolve().parent)


try:
    __all__
except NameError:
    __all__ = []
for _n in ("get_include",):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC lib utils shim ---
