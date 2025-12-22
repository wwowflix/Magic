from __future__ import annotations

from typing import Any, Dict, TypeVar, Callable

# Simple JSON dict alias used by CDP-generated modules
T_JSON_DICT = Dict[str, Any]

Cls = TypeVar("Cls")

def event_class(arg: Any = None) -> Callable[[Cls], Cls] | Cls:
    """
    Flexible decorator used by CDP-generated protocol modules.

    Supports both:

        @event_class
        class Foo: ...

    and:

        @event_class("Runtime.bindingCalled")
        class Foo: ...

    It just attaches a `_cdp_event` attribute to the class so the
    protocol machinery can introspect event types.
    """

    # Case 1: used as @event_class
    if callable(arg):
        cls = arg  # type: ignore[assignment]
        setattr(cls, "_cdp_event", getattr(cls, "__name__", "unknown"))
        return cls  # type: ignore[return-value]

    # Case 2: used as @event_class("Domain.EventName")
    def decorator(cls: Cls) -> Cls:
        setattr(cls, "_cdp_event", str(arg) if arg is not None else getattr(cls, "__name__", "unknown"))
        return cls

    return decorator
# ---- auto-added by MAGIC CDP util shim ----
try:
    _orig_event_class = event_class  # type: ignore[name-defined]
except Exception:
    _orig_event_class = None


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
# ---- end MAGIC CDP util shim ----

# ---- MAGIC CDP helper shim (added by MAGIC) ----
from typing import Any, Dict, TypeVar, Callable, Type

T = TypeVar("T")

# JSON dict alias expected by CDP runtime modules
T_JSON_DICT = Dict[str, Any]


def event_class(arg: object | None = None):
    """
    Flexible decorator used by CDP-generated modules.

    Supports both:
        @event_class
        class Foo: ...

    and:
        @event_class("Runtime.bindingCalled")
        class BindingCalledEvent: ...
    """

    def _decorate(cls: Type[T], event_name: str | None = None) -> Type[T]:
        # Attach a readable marker on the class
        setattr(cls, "_cdp_event", event_name or getattr(cls, "__name__", "unknown"))
        return cls

    # Case 1: used as bare decorator -> @event_class
    if callable(arg):
        return _decorate(arg)  # type: ignore[arg-type]

    # Case 2: used as factory with a name -> @event_class("Runtime.bindingCalled")
    event_name = None if arg is None else str(arg)

    def wrapper(cls: Type[T]) -> Type[T]:
        return _decorate(cls, event_name)

    return wrapper

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
