from __future__ import annotations

# CDP domain: Console
#
# MAGIC note:
# This file is a hybrid:
# - It keeps the CDP-generated API (ConsoleMessage, clear_messages, enable, disable, MessageAdded)
# - It adds a safe MAGIC-compatible event_class decorator
# - It adds Rich-style stubs: Group, RenderableType
#
# Goal: all imports from scripts.console work under tests.

from typing import Any, TypeVar
from dataclasses import dataclass
import typing

from .util import T_JSON_DICT

# ---------------------------------------------------------------------------
# MAGIC shim: event_class decorator
# ---------------------------------------------------------------------------

_T = TypeVar("_T")


def event_class(name_or_cls: Any = None):
    """
    MAGIC-compatible event_class decorator.

    Supports both:
        @event_class("Console.messageAdded")
        class ConsoleMessage: ...

        @event_class
        class ConsoleMessage: ...

    It just attaches __cdp_event_name__ on the class and returns it.
    """

    def _decorate(cls: _T) -> _T:
        if isinstance(name_or_cls, str):
            event_name = name_or_cls
        else:
            event_name = getattr(cls, "__name__", "")
        setattr(cls, "__cdp_event_name__", event_name)
        return cls

    # Used as @event_class
    if callable(name_or_cls) and not isinstance(name_or_cls, str):
        cls = name_or_cls
        return _decorate(cls)

    # Used as @event_class("Domain.eventName")
    return _decorate


# ---------------------------------------------------------------------------
# CDP Console domain data structures
# ---------------------------------------------------------------------------


@dataclass
class ConsoleMessage:
    """
    Console message.
    """

    #: Message source.
    source: str

    #: Message severity.
    level: str

    #: Message text.
    text: str

    #: URL of the message origin.
    url: typing.Optional[str] = None

    #: Line number in the resource that generated this message (1-based).
    line: typing.Optional[int] = None

    #: Column number in the resource that generated this message (1-based).
    column: typing.Optional[int] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = {}
        json["source"] = self.source
        json["level"] = self.level
        json["text"] = self.text
        if self.url is not None:
            json["url"] = self.url
        if self.line is not None:
            json["line"] = self.line
        if self.column is not None:
            json["column"] = self.column
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> "ConsoleMessage":
        return cls(
            source=str(json["source"]),
            level=str(json["level"]),
            text=str(json["text"]),
            url=str(json["url"]) if "url" in json else None,
            line=int(json["line"]) if "line" in json else None,
            column=int(json["column"]) if "column" in json else None,
        )


def clear_messages() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Does nothing (CDP stub).
    """
    cmd_dict: T_JSON_DICT = {
        "method": "Console.clearMessages",
    }
    json = yield cmd_dict
    return None


def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Disables console domain, prevents further console messages from
    being reported to the client. (CDP stub)
    """
    cmd_dict: T_JSON_DICT = {
        "method": "Console.disable",
    }
    json = yield cmd_dict
    return None


def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Enables console domain, sends the messages collected so far to the
    client by means of the ``messageAdded`` notification. (CDP stub)
    """
    cmd_dict: T_JSON_DICT = {
        "method": "Console.enable",
    }
    json = yield cmd_dict
    return None


@event_class("Console.messageAdded")
@dataclass
class MessageAdded:
    """
    Issued when new console message is added.
    """

    #: Console message that has been added.
    message: ConsoleMessage

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> "MessageAdded":
        return cls(message=ConsoleMessage.from_json(json["message"]))


# ---------------------------------------------------------------------------
# MAGIC shim: Rich-style Group & RenderableType
# ---------------------------------------------------------------------------

from typing import List  # noqa: E402  (keep imports after CDP section)

RenderableType = Any


class Group:
    """
    MAGIC stub for a "Group" renderable.

    In real Rich, this groups multiple renderables so they are treated as a
    single unit. For MAGIC we just keep the list; any code that inspects or
    iterates over it will still behave sensibly.
    """

    def __init__(self, *renderables: RenderableType) -> None:
        self.renderables: List[RenderableType] = list(renderables)

    def __iter__(self):
        return iter(self.renderables)

    def __repr__(self) -> str:
        return f"<MAGIC Group renderables={len(self.renderables)}>"

# Export public symbols
__all__ = [
    "ConsoleMessage",
    "clear_messages",
    "disable",
    "enable",
    "MessageAdded",
    "event_class",
    "Group",
    "RenderableType",
]


# MAGIC shim: minimal Console / get_console for rich-like helpers
try:
    Console  # type: ignore[name-defined]
    get_console  # type: ignore[name-defined]
except NameError:
    class Console:
        def print(self, *objects: object, **kwargs: object) -> None:
            """Very small print wrapper used in MAGIC shims."""
            print(*objects)

        def log(self, *objects: object, **kwargs: object) -> None:
            print(*objects)

    _GLOBAL_CONSOLE: "Console | None" = None  # type: ignore[valid-type]

    def get_console() -> Console:
        global _GLOBAL_CONSOLE
        if _GLOBAL_CONSOLE is None:
            _GLOBAL_CONSOLE = Console()
        return _GLOBAL_CONSOLE
# ===== MAGIC compatibility shim appended at end of console.py =====

# This block is SAFE to append. It only defines symbols if they do not
# already exist earlier in this module, so the original implementation
# keeps full control when present.

from typing import Any, Iterable, Optional
try:
    from dataclasses import dataclass
except Exception:  # very defensive, should not normally happen
    dataclass = None  # type: ignore[assignment]

# Fallback Console if none was defined above
try:
    Console  # type: ignore[name-defined]
except NameError:  # pragma: no cover - only used in MAGIC stub case
    class Console:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            # minimal stand-in; real rich.Console is much richer
            self._options = kwargs

        def print(self, *args: Any, **kwargs: Any) -> None:
            # For smoke tests we don't need actual terminal rendering.
            # You could log or ignore; here we just no-op.
            return None


# Minimal ConsoleOptions so `from scripts.console import ConsoleOptions` works
try:
    ConsoleOptions  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    if dataclass is not None:
        @dataclass
        class ConsoleOptions:  # type: ignore[no-redef]
            legacy_windows: bool = False
            color_system: Optional[str] = None
            min_width: int = 0
            max_width: int = 80
    else:
        class ConsoleOptions:  # type: ignore[no-redef]
            def __init__(
                self,
                legacy_windows: bool = False,
                color_system: Optional[str] = None,
                min_width: int = 0,
                max_width: int = 80,
            ) -> None:
                self.legacy_windows = legacy_windows
                self.color_system = color_system
                self.min_width = min_width
                self.max_width = max_width


# Minimal RenderResult alias (rich uses an iterable of renderables)
try:
    RenderResult  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    RenderResult = Iterable[Any]
# ===== end MAGIC compatibility shim =====

# ======================================================================
# MAGIC Week 0 shim – JustifyMethod enum for console layout
# ======================================================================

from enum import Enum, auto


class JustifyMethod(Enum):
    """
    Very small enum used by scripts.syntax / console rendering.

    Week 0 goal:
    - Provide symbolic names so imports from `scripts.syntax` and
      `scripts.drawing` succeed.
    - We do NOT implement any real layout or rendering here.
    """
    LEFT   = auto()
    CENTER = auto()
    RIGHT  = auto()
    FULL   = auto()
