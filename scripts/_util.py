from __future__ import annotations

"""
MAGIC shim for internal utility helpers required by multiple vendored modules.

Provides:

- Filesystem helpers:
    * ensure_directory_exists
    * is_writable
    * raise_on_not_writable_file

- Thread / main-thread helper:
    * is_main_thread

- Async generator helper:
    * name_asyncgen

- CDP-style decorator + JSON type:
    * event_class
    * T_JSON_DICT

- Trio-style channel utilities:
    * MultipleExceptionError
    * NoPublicConstructor (as a METACLASS, subclassing ABCMeta)
    * final
    * generic_function
    * raise_single_exception_from_group
    * ConflictDetector

- HTTP/headers helpers (h11-style):
    * LocalProtocolError
    * RemoteProtocolError
    * Sentinel   (CALLABLE, so code can do Sentinel("NEED_DATA"))
    * bytesify
    * validate

- Async helper:
    * async_wraps  (used by _file_io)

- AUTO-STUB REGION:
    Any extra symbols imported from scripts that live in scripts/_util.py
    but not defined above will be auto-generated as stubs by the MAGIC
    PowerShell fixer. See bottom of file.

Goal: 100% import-safe, minimal behavior, no heavy dependencies.
"""

import os
import abc
import threading
from typing import Any, Iterable, Dict as _Dict, Any as _Any, Callable


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def ensure_directory_exists(path: str) -> str:
    """Creates directory if it doesn't exist, returns the path."""
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        # Never let directory creation break imports.
        pass
    return path


def is_writable(path: str) -> bool:
    """Return True if path is writable."""
    try:
        test_path = os.path.join(path, ".magic_write_test")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(test_path)
        return True
    except Exception:
        return False


def raise_on_not_writable_file(path: str) -> None:
    """Raise a RuntimeError if the directory for this file is not writable."""
    dir_path = os.path.dirname(path) or "."
    if not is_writable(dir_path):
        raise RuntimeError(f"Path not writable: {path}")


# ---------------------------------------------------------------------------
# Thread / main-thread helper
# ---------------------------------------------------------------------------

def is_main_thread() -> bool:
    """
    Lightweight helper used by ki/windows IO code.

    Returns True if current thread is the main thread.
    """
    try:
        return threading.current_thread() is threading.main_thread()
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Async generator helper
# ---------------------------------------------------------------------------

def name_asyncgen(agen: Any, name: str | None) -> Any:
    """
    MAGIC shim for async generator naming.

    The real implementation would tweak debug metadata. For MAGIC, we only
    need this function to exist and be safe. It tries to attach a __name__
    attribute and then returns the async generator unchanged.
    """
    try:
        if name:
            setattr(agen, "__name__", str(name))
    except Exception:
        # Never break execution just because metadata assignment failed.
        pass
    return agen


# ---------------------------------------------------------------------------
# CDP-style event_class + JSON dict type
# ---------------------------------------------------------------------------

def event_class(arg=None):
    """
    MAGIC shim for CDP-style @event_class decorator.

    Supports both usage forms:

    - @event_class
      class MyEvent: ...

    - @event_class("Runtime.bindingCalled")
      class MyEvent: ...
    """

    def decorator(cls):
        # If used as @event_class("Some.EventName"), attach metadata.
        if isinstance(arg, str):
            try:
                setattr(cls, "_event_name", arg)
            except Exception:
                # Never let metadata issues break imports.
                pass
        return cls

    # If used as bare @event_class with no parentheses,
    # then `arg` *is* the class object.
    if callable(arg) and not isinstance(arg, str):
        return decorator(arg)

    # If used with an explicit argument (e.g. a string),
    # return a real decorator.
    return decorator


try:
    T_JSON_DICT = _Dict[str, _Any]
except Exception:  # pragma: no cover
    T_JSON_DICT = dict  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Trio-style channel / error helpers
# ---------------------------------------------------------------------------

class MultipleExceptionError(Exception):
    """
    Simple container for multiple exceptions.

    The real trio version preserves a lot more detail; for MAGIC we just
    store them on .exceptions and format a basic message.
    """
    def __init__(self, exceptions: Iterable[BaseException]) -> None:
        self.exceptions = list(exceptions)
        msg = f"{len(self.exceptions)} exceptions raised"
        super().__init__(msg)


class NoPublicConstructor(abc.ABCMeta):
    """
    Metaclass used in trio-like code to prevent public instantiation.

    NOTE: this must be a METACLASS and must subclass ABCMeta (or type)
    so it plays nicely with trio.abc.Channel's own metaclass.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover
        # In real trio, this raises a TypeError when someone tries to instantiate
        # a class that uses this metaclass directly.
        raise TypeError(f"{cls.__name__} has no public constructor")


def final(obj: Any) -> Any:
    """
    MAGIC shim for @final decorator.

    In type-checking land this prevents subclassing; at runtime, we just
    return the object unchanged.
    """
    return obj


def generic_function(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    MAGIC shim for a generic_function decorator.

    Used mainly for typing; here it just returns the function unchanged.
    """
    return func


def raise_single_exception_from_group(exceptions: Iterable[BaseException]) -> None:
    """
    Raise the first exception from an iterable.

    The full trio implementation has more sophisticated logic. For MAGIC,
    raising the first one is sufficient and keeps behaviour simple.
    """
    for exc in exceptions:
        raise exc
    # If the iterable is empty, do nothing.


class ConflictDetector:
    """
    Lightweight ConflictDetector used by high-level socket helpers.

    The real trio version enforces that certain resources are not used
    concurrently in conflicting ways. For MAGIC, we simply track a boolean
    and provide context manager hooks so that:

        with ConflictDetector("name"):
            ...

    works without raising errors.
    """

    def __init__(self, name: str = "resource") -> None:
        self._name = name
        self._active = False

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ConflictDetector {self._name!r} active={self._active}>"

    # Basic API shims (not strict, just best-effort)

    def check_in(self) -> None:
        self._active = True

    def check_out(self) -> None:
        self._active = False

    # Context manager protocol

    def __enter__(self) -> "ConflictDetector":
        self.check_in()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.check_out()


# ---------------------------------------------------------------------------
# HTTP/headers helpers (h11-style)
# ---------------------------------------------------------------------------

class LocalProtocolError(Exception):
    """
    Minimal LocalProtocolError used by HTTP header/connection code.

    We optionally store an error_code attribute if provided; otherwise,
    this behaves like a normal Exception.
    """
    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        self.error_code = error_code


class RemoteProtocolError(LocalProtocolError):
    """
    Minimal RemoteProtocolError for peer-originated protocol errors.
    Subclasses LocalProtocolError to satisfy isinstance checks.
    """
    pass


class Sentinel:
    """
    Simple callable sentinel type used by HTTP reader/connection code.

    The real h11 Sentinel tracks a name and is used for identity
    comparisons. For MAGIC we just keep the name and a nice repr.

    NOTE: this is a CLASS, not a pre-created instance.
    That means code like `NEED_DATA = Sentinel("NEED_DATA")` works.
    """
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover
        return f"<MAGIC-SENTINEL {self.name!r}>"


def bytesify(value: Any) -> bytes:
    """
    Convert value to bytes in a tolerant way.

    - If already bytes/bytearray -> bytes
    - If str -> ASCII/latin-1 encoded
    - Otherwise -> str(value).encode(...)
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        try:
            return value.encode("ascii")
        except UnicodeEncodeError:
            return value.encode("latin-1", "replace")
    text = str(value)
    try:
        return text.encode("ascii")
    except UnicodeEncodeError:
        return text.encode("latin-1", "replace")


def validate(*args: Any, **kwargs: Any) -> None:
    """
    MAGIC stub for validate() used by header/connection modules.

    In real implementations, this enforces protocol rules.
    For MAGIC we treat it as a no-op that never raises.
    """
    return None


# ---------------------------------------------------------------------------
# Async helper for file I/O wrapper (async_wraps)
# ---------------------------------------------------------------------------

def async_wraps(wrapped: Callable[..., Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Lightweight async-aware wraps decorator used by _file_io.

    Behaviour:
      - Preserves basic metadata (__name__, __doc__, __module__, __qualname__,
        __annotations__) on the wrapper.
      - Does NOT change call semantics; it simply returns the wrapper.

    This is enough for trio-style helpers that just need a decorator symbol
    called async_wraps.
    """

    def decorator(wrapper: Callable[..., Any]) -> Callable[..., Any]:
        try:
            for attr in ("__name__", "__doc__", "__module__", "__qualname__", "__annotations__"):
                if hasattr(wrapped, attr):
                    setattr(wrapper, attr, getattr(wrapped, attr))
        except Exception:
            # Never fail just because metadata couldn't be copied.
            pass
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# MAGIC AUTO-STUBS SECTION
# (appended by PowerShell fixer if extra symbols are imported from _util)
# ---------------------------------------------------------------------------



# ---- MAGIC: override event_class decorator to support arguments ----
try:
    from typing import Dict, Any
except Exception:  # super defensive fallback
    Dict = dict  # type: ignore
    Any = object  # type: ignore

def event_class(arg=None):
    """
    Flexible decorator used by CDP-generated protocol modules.

    Supports both:

        @event_class
        class Foo: ...

    and:

        @event_class("Runtime.bindingCalled")
        class Foo: ...

    It simply attaches a _cdp_event attribute to the class, which
    the generated runtime/accessibility/dom/page code expects.
    """
    # Case 1: used as @event_class
    if callable(arg):
        cls = arg
        setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
        return cls

    # Case 2: used as @event_class("Some.Name")
    def decorator(cls):
        setattr(cls, "_cdp_event", str(arg) if arg is not None else getattr(cls, "__name__", "unknown"))
        return cls

    return decorator
# ---- MAGIC: override event_class decorator to support arguments ----
try:
    from typing import Any, Dict
except Exception:  # super defensive fallback
    Any = object  # type: ignore
    Dict = dict   # type: ignore

def event_class(arg=None):
    """
    Flexible decorator used by CDP-generated protocol modules.

    Supports both:

        @event_class
        class Foo: ...

    and:

        @event_class("Runtime.bindingCalled")
        class Foo: ...

    It simply attaches a _cdp_event attribute to the class.
    """
    # Case 1: used as @event_class
    if callable(arg):
        cls = arg
        setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
        return cls

    # Case 2: used as @event_class("Some.Name")
    def decorator(cls):
        setattr(cls, "_cdp_event", str(arg) if arg is not None else getattr(cls, "__name__", "unknown"))
        return cls

    return decorator
# ---- MAGIC: override event_class decorator to support arguments ----
try:
    from typing import Any, Dict
except Exception:  # super defensive fallback
    Any = object  # type: ignore
    Dict = dict   # type: ignore

def event_class(arg=None):
    """
    Flexible decorator used by CDP-generated protocol modules.

    Supports both:

        @event_class
        class Foo: ...

    and:

        @event_class("Runtime.bindingCalled")
        class Foo: ...

    It simply attaches a _cdp_event attribute to the class.
    """
    # Case 1: used as @event_class
    if callable(arg):
        cls = arg
        setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
        return cls

    # Case 2: used as @event_class("Some.Name")
    def decorator(cls):
        setattr(cls, "_cdp_event", str(arg) if arg is not None else getattr(cls, "__name__", "unknown"))
        return cls

    return decorator
