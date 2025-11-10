from __future__ import annotations

"""MAGIC shim: minimal distlib-like util surface for imports only."""
from dataclasses import dataclass
from functools import cached_property as _cached_property  # re-exported
from pathlib import Path
from typing import Optional, Any

# Re-export name expected by "from .util import cached_property, get_cache_base, Cache"
cached_property = _cached_property  # noqa: N816


def get_cache_base(suffix: Optional[str] = None) -> str:
    base = Path(".") / ".magic_cache"
    base.mkdir(parents=True, exist_ok=True)
    if suffix:
        base = base / str(suffix)
        base.mkdir(parents=True, exist_ok=True)
    return str(base)


@dataclass
class Cache:
    base: str

    def __post_init__(self) -> None:
        Path(self.base).mkdir(parents=True, exist_ok=True)


# --------- extra helpers some modules import from "util" ---------


class FileOperator:
    """Very small stub used only during import-time; methods are no-ops."""

    def write_text(self, path: str, text: str, encoding: str = "utf-8") -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding=encoding)

    def write_binary(self, path: str, data: bytes) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def is_writable(self, path: str) -> bool:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            test = p.with_suffix(p.suffix + ".tmp")
            test.write_bytes(b"")
            test.unlink(missing_ok=True)
            return True
        except Exception:
            return False


def get_export_entry(s: str) -> str:
    # Import-time only; return unchanged
    return s


def convert_path(p: Any) -> str:
    return str(p)


def get_executable() -> str:
    import sys

    return sys.executable


def get_platform() -> str:
    import sys

    return sys.platform


def in_venv() -> bool:
    import sys, os

    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        or bool(os.environ.get("VIRTUAL_ENV"))
    )


__all__ = [
    "cached_property",
    "get_cache_base",
    "Cache",
    "FileOperator",
    "get_export_entry",
    "convert_path",
    "get_executable",
    "get_platform",
    "in_venv",
]
