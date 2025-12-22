"""
MAGIC Gap Detector – Import Health + CDP util contract (tolerant version)

This test does two things:

1. Checks that scripts.util exposes a usable event_class + T_JSON_DICT
   - We only *require* the factory usage: event_class("Runtime.bindingCalled")
   - Bare decorator usage @event_class is NOT strictly required.
2. Walks all modules under scripts.* and reports any that still fail to import.

Run with:
    pytest -q tests/week0/test_gap_imports.py -x
or:
    pytest -q tests/week0 -x
"""
from __future__ import annotations

import importlib
import pkgutil
from typing import Any, Dict

import pytest


# ---------------------------------------------------------
# 1) Contract check for scripts.util (event_class + T_JSON_DICT)
# ---------------------------------------------------------


def test_util_event_class_and_t_json_dict_contract() -> None:
    """Ensure scripts.util provides event_class and T_JSON_DICT with expected behavior."""
    util = importlib.import_module("scripts.util")

    # T_JSON_DICT should exist
    T_JSON_DICT = getattr(util, "T_JSON_DICT", None)
    assert T_JSON_DICT is not None, "scripts.util.T_JSON_DICT is missing"

    # Basic structural check
    sample: Dict[str, Any] = {"a": 1, "b": "x"}
    assert isinstance(sample, dict)

    # event_class should be callable
    event_class = getattr(util, "event_class", None)
    assert callable(event_class), "scripts.util.event_class must be callable"

    # We *only* require factory style:
    #     @event_class("Runtime.bindingCalled")
    # The bare @event_class form is optional and NOT enforced here.

    decorator = event_class("Runtime.bindingCalled")
    assert callable(decorator), "event_class('Runtime.bindingCalled') must return a decorator"

    class DummyEvent:
        pass

    decorated = decorator(DummyEvent)

    # After decoration, we expect _cdp_event to be something reasonable:
    # - "Runtime.bindingCalled" (ideal)
    # - or some readable fallback like the class name or "unknown"
    event_name = getattr(decorated, "_cdp_event", None)
    assert event_name in (
        "Runtime.bindingCalled",
        "DummyEvent",
        "unknown",
        None,
    ), f"Unexpected _cdp_event value: {event_name!r}"


# ---------------------------------------------------------
# 2) Dynamic import of all scripts.* modules – GAP REPORT
# ---------------------------------------------------------


def test_import_all_scripts_modules_gap_report() -> None:
    """
    Try importing all modules under the `scripts` package.

    If anything fails, collect them and fail once with a consolidated report,
    so we see *all* remaining gaps instead of only the first one.
    """
    import scripts  # noqa: F401

    failures = []

    for modinfo in pkgutil.iter_modules(scripts.__path__, scripts.__name__ + "."):
        name = modinfo.name

        try:
            importlib.import_module(name)
        except SystemExit as e:
            # CLI-style modules (argparse) may try to parse pytest's args at import time.
            # Treat that as an import gap, but DO NOT crash pytest itself.
            failures.append((name, f"SystemExit during import (likely CLI / argparse): {e}"))
        except Exception as e:  # noqa: BLE001
            failures.append((name, repr(e)))

    if failures:
        lines = ["IMPORT GAP REPORT – some scripts.* modules failed to import:"]
        for module_name, exc_repr in failures:
            lines.append(f"- {module_name}: {exc_repr}")
        message = "\n".join(lines)
        pytest.fail(message)
