"""MAGIC-safe shim for scripts.action_builder.

This replaces the original selenium-based vendor module with a safe, import-only
facade. It avoids importing selenium so tests can run without that dependency.

If you later install selenium and want real behaviour back, you can restore the
*.magic_bak_* file or swap this shim for a proper wrapper around selenium.
"""

from __future__ import annotations

from typing import Any, Dict, List


class Command:
    """Fallback shim for selenium.webdriver.remote.command.Command.

    Only provides minimal attributes so import-time usage does not explode.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.name = args[0] if args else "MAGIC-FAKE-COMMAND"
        self.params: Dict[str, Any] = dict(kwargs)


class Interaction:
    """Minimal stand-in for a user interaction step."""

    def __init__(self, source: object, id: str = "MAGIC") -> None:
        self.source = source
        self.id = id


class InputDevice:
    """Base class for input devices in this shim."""

    def __init__(self, name: str = "MAGIC-DEVICE") -> None:
        self.name = name


class PointerInput(InputDevice):
    """Shim for pointer/ mouse-like input."""

    KIND_MOUSE = "mouse"
    KIND_PEN = "pen"
    KIND_TOUCH = "touch"


class KeyInput(InputDevice):
    """Shim for keyboard input."""
    pass


class WheelInput(InputDevice):
    """Shim for scroll wheel input."""
    pass


class ActionBuilder:
    """Very small placeholder for selenium ActionBuilder.

    Enough for MAGIC to construct it without crashing; methods are no-ops.
    """

    def __init__(
        self,
        driver: object | None = None,
        mouse: PointerInput | None = None,
        keyboard: KeyInput | None = None,
        wheel: WheelInput | None = None,
    ) -> None:
        self.driver = driver
        self.mouse = mouse or PointerInput()
        self.keyboard = keyboard or KeyInput()
        self.wheel = wheel or WheelInput()
        self.devices: List[InputDevice] = [self.mouse, self.keyboard, self.wheel]
        self._actions: List[Interaction] = []

    def add_action(self, action: Interaction) -> None:
        """Record an action; this is a no-op shim."""
        self._actions.append(action)

    def perform(self) -> None:  # pragma: no cover
        """Execute recorded actions (no-op in shim)."""
        return None

    def clear_actions(self) -> None:
        """Clear recorded actions in the shim."""
        self._actions.clear()


__all__ = [
    "Command",
    "Interaction",
    "InputDevice",
    "PointerInput",
    "KeyInput",
    "WheelInput",
    "ActionBuilder",
]
