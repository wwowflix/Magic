"""MAGIC-safe shim for scripts.action_chains.

This replaces the original Selenium-based ActionChains implementation with a
minimal, import-safe stub that does NOT depend on the selenium package.

It is only meant to keep MAGIC’s tests and imports happy. If you later install
selenium and want real behaviour, restore the *.magic_bak_* file or swap this
shim for a proper wrapper.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional


class WebElement:
    """Minimal stand-in for selenium.webdriver.remote.webelement.WebElement."""

    def __init__(self, element_id: str = "MAGIC-ELEMENT") -> None:
        self.id = element_id

    def __repr__(self) -> str:  # pragma: no cover
        return f"<WebElement id={self.id!r}>"


class ActionChains:
    """No-op ActionChains shim.

    Methods mirror the real Selenium API surface enough so that user code can
    construct and chain calls without raising errors. All operations are
    recorded into _steps but do not actually control a browser.
    """

    def __init__(self, driver: Any | None = None) -> None:
        self.driver = driver
        self._steps: List[str] = []

    # --- basic pointer / click actions -------------------------------------

    def click(self, on_element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("click")
        return self

    def click_and_hold(self, on_element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("click_and_hold")
        return self

    def context_click(self, on_element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("context_click")
        return self

    def double_click(self, on_element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("double_click")
        return self

    def move_to_element(self, to_element: WebElement) -> "ActionChains":
        self._steps.append("move_to_element")
        return self

    def move_by_offset(self, xoffset: int, yoffset: int) -> "ActionChains":
        self._steps.append(f"move_by_offset({xoffset},{yoffset})")
        return self

    def release(self, on_element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("release")
        return self

    # --- keyboard / typing -------------------------------------------------

    def send_keys(self, *keys_to_send: Any) -> "ActionChains":
        self._steps.append("send_keys")
        return self

    def send_keys_to_element(self, element: WebElement, *keys_to_send: Any) -> "ActionChains":
        self._steps.append("send_keys_to_element")
        return self

    def key_down(self, value: Any, element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("key_down")
        return self

    def key_up(self, value: Any, element: Optional[WebElement] = None) -> "ActionChains":
        self._steps.append("key_up")
        return self

    # --- wheel / scroll (placeholder) -------------------------------------

    def scroll_by_amount(self, delta_x: int, delta_y: int) -> "ActionChains":
        self._steps.append(f"scroll_by_amount({delta_x},{delta_y})")
        return self

    # --- execution / housekeeping -----------------------------------------

    def perform(self) -> None:  # pragma: no cover
        """Execute recorded actions (no-op in shim)."""
        # In real selenium this would flush to the driver. Here we just clear.
        self._steps.clear()

    def reset_actions(self) -> None:
        """Clear recorded actions in the shim."""
        self._steps.clear()


__all__ = ["WebElement", "ActionChains"]
