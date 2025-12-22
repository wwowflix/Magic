# =============================================================================
# MAGIC shims: compatibility helpers for core.py/actions/data imports
# =============================================================================

from __future__ import annotations

from functools import lru_cache
from typing import Any, Iterable, Callable, TypeVar
import warnings


# -----------------------------------------------------------------------------
# FIFO / unbounded caches and helper utilities
# -----------------------------------------------------------------------------
# Only define these if they are missing, so we don't override any real versions.
try:
    _FifoCache  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    class _FifoCache(dict):
        """
        Minimal FIFO-style cache:
        - Stores up to maxsize entries
        - Clears itself when full (simple behaviour; good enough for placeholders)
        """
        def __init__(self, maxsize: int = 128):
            super().__init__()
            self.maxsize = maxsize

        def get_or_create(self, key, creator):
            if key in self:
                return self[key]
            value = creator()
            if len(self) >= self.maxsize:
                # Simple behaviour: reset when full
                self.clear()
            self[key] = value
            return value

    class _UnboundedCache(dict):
        """
        Unbounded cache: grows as needed, never evicts.
        """
        def get_or_create(self, key, creator):
            if key in self:
                return self[key]
            value = creator()
            self[key] = value
            return value

    def _collapse_string_to_ranges(s: str) -> str:
        """
        Placeholder implementation – currently just returns the input string.
        Real implementations may compress character ranges; we don't need that yet.
        """
        return s

    def _escape_regex_range_chars(s: str) -> str:
        """
        No-op placeholder for now – in real usage this would escape regex range chars.
        """
        return s

    def _bslash(s: str) -> str:
        """Return the string prefixed with a backslash."""
        return "\\" + s

    def _flatten(iterable: Iterable[Any]):
        """
        Simple recursive flattener for nested iterables (lists/tuples/sets).
        Non-iterable items are yielded as-is.
        """
        from collections.abc import Iterable as _Iterable

        for item in iterable:
            if isinstance(item, (list, tuple, set)):
                for sub in _flatten(item):
                    yield sub
            else:
                yield item

    class LRUMemo(_FifoCache):
        """Alias compatible with expected LRUMemo type."""
        pass

    class UnboundedMemo(_UnboundedCache):
        """Alias compatible with expected UnboundedMemo type."""
        pass


# -----------------------------------------------------------------------------
# __config_flags: pyparsing-style configuration flags base class
# -----------------------------------------------------------------------------
# core.py does: `class __compat__(__config_flags): ...`
# so we must supply a class with the right basic API.
try:
    __config_flags  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    C = TypeVar("C", bound=Callable[..., object])

    class __config_flags:
        """Internal class for defining compatibility/debug flags.

        This mirrors pyparsing.util.__config_flags enough for
        scripts.core.__compat__ to subclass it safely.
        """

        _all_names: list[str] = []
        _fixed_names: list[str] = []
        _type_desc: str = "configuration"

        @classmethod
        def _set(cls, dname: str, value: bool) -> None:
            if dname in cls._fixed_names:
                warnings.warn(
                    f"{cls.__name__}.{dname} {cls._type_desc} is "
                    f"{str(getattr(cls, dname)).upper()} and cannot be overridden",
                    stacklevel=3,
                )
                return
            if dname in cls._all_names:
                setattr(cls, dname, value)
            else:
                raise ValueError(f"no such {cls._type_desc} {dname!r}")

        @classmethod
        def enable(cls, name: str) -> None:
            cls._set(name, True)

        @classmethod
        def disable(cls, name: str) -> None:
            cls._set(name, False)


# -----------------------------------------------------------------------------
# col: pyparsing-style column helper (NOT the older "pick column from row")
# -----------------------------------------------------------------------------
# Only define col if it doesn't already exist, so we don't override real code.
try:
    col  # type: ignore[name-defined]
except NameError:  # pragma: no cover

    @lru_cache(maxsize=128)
    def col(loc: int, strg: str) -> int:
        """
        Return 1-based column number given a 0-based `loc` in the string `strg`.

        This matches pyparsing.util.col, which is what scripts/actions/core/data
        expect for error reporting and debug helpers.
        """
        if loc <= 0:
            return 1

        # Find last newline before loc and compute distance from it
        last_nl = strg.rfind("\n", 0, loc)
        if last_nl < 0:
            # No newline before loc -> column is loc+1
            return loc + 1

        return loc - last_nl


# =============================================================================
# End MAGIC shims
# =============================================================================

# ==== MAGIC shim: distlib util compatibility layer for Scripts/resources ====
import os as _MAGIC_os
import tempfile as _MAGIC_tempfile
from typing import Any as _MAGIC_Any

# Provide a cached_property compatible with distlib.util.cached_property
try:
    from functools import cached_property as _MAGIC_cached_property
except Exception:  # very old or weird Python
    def _MAGIC_cached_property(func):  # type: ignore
        # Fallback: simple property
        return property(func)

cached_property = _MAGIC_cached_property  # re-export

def get_cache_base():
    """MAGIC shim: return a writable base directory for cache usage."""
    return _MAGIC_tempfile.gettempdir()

class Cache:
    """Minimal Cache stub for distlib.resources.

    This is intentionally tiny: it keeps Scripts/resources imports happy.
    It stores base_dir and name, and offers prefix_to_dir().
    """
    def __init__(self, base_dir: str | None = None, name: str | None = None) -> None:
        self.base_dir = base_dir or get_cache_base()
        self.name = name or "cache"

    def prefix_to_dir(self, prefix: str) -> str:
        """Return a directory path for a given cache prefix."""
        return _MAGIC_os.path.join(self.base_dir, prefix)

    def __repr__(self) -> str:
        return f"<Cache base_dir={self.base_dir!r} name={self.name!r}>"

# ==== end MAGIC shim ====


# ==== MAGIC shim: extra distlib util symbols for Scripts ====
import os as _MAGIC_os2
import sys as _MAGIC_sys2
try:
    import sysconfig as _MAGIC_sysconfig2
except Exception:
    _MAGIC_sysconfig2 = None

class FileOperator:
    """Minimal FileOperator stub for Scripts module.

    Designed just to keep imports and basic usage happy.
    """
    def __init__(self, *args, **kwargs):
        self.dry_run = kwargs.get("dry_run", False)

    def __call__(self, *args, **kwargs):
        # Real distlib does file operations; we no-op here.
        return None

def get_export_entry(spec: str):
    """MAGIC shim: return export spec unchanged."""
    return spec

def convert_path(path: str) -> str:
    """Convert forward slashes to OS-specific separators."""
    return path.replace("/", _MAGIC_os2.sep)

def get_executable() -> str:
    """Return current Python executable path."""
    return _MAGIC_sys2.executable

def get_platform() -> str:
    """Return a reasonable platform tag."""
    if _MAGIC_sysconfig2 is not None:
        try:
            return _MAGIC_sysconfig2.get_platform()
        except Exception:
            pass
    return _MAGIC_sys2.platform

def in_venv() -> bool:
    """Detect if running inside a virtualenv."""
    return (
        hasattr(_MAGIC_sys2, "base_prefix")
        and _MAGIC_sys2.base_prefix != _MAGIC_sys2.prefix
    )
# ==== end MAGIC shim: extra distlib util symbols ====

# ---- auto-added by MAGIC CDP util shim ----
try:
    _orig_event_class = event_class  # type: ignore[name-defined]
except Exception:
    _orig_event_class = None  # type: ignore[assignment]


def event_class(arg=None):
    """
    Flexible decorator to tag CDP event classes.

    Supports:
    - @event_class
    - @event_class("Runtime.bindingCalled")
    - event_class(MyCls)  # direct call

    It sets a `_cdp_event` attribute on the class.
    """
    # Case: @event_class("Name")
    if isinstance(arg, str):
        event_name = arg

        def decorator(cls):
            setattr(cls, "_cdp_event", event_name or getattr(cls, "__name__", "unknown"))
            return cls

        return decorator

    # Case: @event_class
    if arg is None:
        def decorator(cls):
            setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
            return cls

        return decorator

    # Case: event_class(MyCls) – direct call with class
    cls = arg
    setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
    return cls


# Ensure T_JSON_DICT exists as a Dict[str, Any]-like alias
try:
    T_JSON_DICT  # type: ignore[name-defined]
except Exception:
    from typing import Any, Dict as _Dict  # type: ignore[import]
    T_JSON_DICT = _Dict[str, Any]  # type: ignore[valid-type]
# ---- end MAGIC CDP util shim ----
