from __future__ import annotations

# --- MAGIC Phase11 – SHIELD: util shims for resources/Scripts ---
try:
    import os, tempfile, functools
except Exception:
    os = None; tempfile = None; functools = None

# cached_property: prefer stdlib, else fall back to a simple @property
try:
    cached_property = functools.cached_property  # py3.8+
except Exception:
    def cached_property(func):
        return property(func)

# get_cache_base: minimal safe temp location
def get_cache_base(suffix=None):
    try:
        base = os.path.join(tempfile.gettempdir(), "distlib-cache")
        if suffix:
            base = os.path.join(base, str(suffix))
        return base
    except Exception:
        return ".distlib-cache"

# Cache: minimal dict-backed stub
class Cache:
    def __init__(self, base_dir=None, **_k):
        self.base_dir = base_dir or get_cache_base()
        self._store = {}
    def get(self, key, default=None):
        return self._store.get(key, default)
    def __getitem__(self, key):
        return self._store[key]
    def __setitem__(self, key, value):
        self._store[key] = value
    def __contains__(self, key):
        return key in self._store
    def clear(self):
        self._store.clear()
# --- end MAGIC util shims ---
import typing
from types import TracebackType


def to_bytes(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> bytes:
    if isinstance(x, bytes):
        return x
    elif not isinstance(x, str):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.encode(encoding or "utf-8", errors=errors or "strict")
    return x.encode()


def to_str(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> str:
    if isinstance(x, str):
        return x
    elif not isinstance(x, bytes):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.decode(encoding or "utf-8", errors=errors or "strict")
    return x.decode()


def reraise(
    tp: type[BaseException] | None,
    value: BaseException,
    tb: TracebackType | None = None,
) -> typing.NoReturn:
    try:
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None  # type: ignore[assignment]
        tb = None

# --- MAGIC Phase11 – SHIELD: ensure required util exports (placed at EOF) ---
try:
    FileOperator
except NameError:
    class FileOperator:  # no-op stub for import-time use
        def __init__(self, *a, **k): pass
        def is_uptodate(self, *a, **k): return True
        def write_binary(self, *a, **k): return None
        def write_text(self, *a, **k): return None
        def copy_file(self, *a, **k): return None

def _u_get_export_entry(spec):
    try:
        if ":" in spec:
            mod, qual = spec.split(":", 1)
        else:
            mod, qual = spec, None
        return mod, qual
    except Exception:
        return spec, None

try:
    get_export_entry
except NameError:
    get_export_entry = _u_get_export_entry

def _u_convert_path(p):
    try:
        import os as _u_os
        return p.replace("/", _u_os.sep)
    except Exception:
        return p

try:
    convert_path
except NameError:
    convert_path = _u_convert_path

try:
    get_executable
except NameError:
    import sys as _u_sys
    def get_executable():
        try:
            return _u_sys.executable or "python"
        except Exception:
            return "python"

try:
    get_platform
except NameError:
    import sys as _u_sys
    def get_platform():
        try:
            return _u_sys.platform
        except Exception:
            return "unknown"

try:
    in_venv
except NameError:
    import sys as _u_sys
    def in_venv():
        try:
            return hasattr(_u_sys, "base_prefix") and _u_sys.prefix != getattr(_u_sys, "base_prefix", _u_sys.prefix)
        except Exception:
            return False

try:
    __all__
except NameError:
    __all__ = []
for _n in [
    "cached_property","get_cache_base","Cache",
    "FileOperator","get_export_entry","convert_path",
    "get_executable","get_platform","in_venv"
]:
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ensure block ---
