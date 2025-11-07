from __future__ import annotations

# --- MAGIC models shim (Headers) ---
from typing import Iterable, Mapping, MutableMapping, Tuple


class Headers(dict[str, str]):
    # Minimal dict-like headers, normalized to str/str
    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            src = args[0]
            if isinstance(src, Mapping):
                for k, v in src.items():
                    self[k] = str(v) if v is not None else ""
            else:
                for k, v in src:  # Iterable[Tuple[str, str]]
                    self[k] = str(v) if v is not None else ""
        for k, v in kwargs.items():
            self[k] = str(v) if v is not None else ""

    @classmethod
    def from_pairs(
        cls, pairs: Iterable[Tuple[str, str]] | Mapping[str, str] | None = None
    ) -> "Headers":
        return cls(pairs or {})


try:
    __all__
except NameError:
    __all__ = []
if "Headers" not in __all__:
    __all__.append("Headers")
# --- end MAGIC models shim (Headers) ---
