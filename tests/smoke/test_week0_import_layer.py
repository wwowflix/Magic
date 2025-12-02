"""
MAGIC Week-0 Import Layer Verification

This test is a *summary check* for Stage 1 (Import Layer Stabilization).

It DOES NOT replace all detailed smokes. Instead, it quickly answers:
- Are the key Week-0 shims present?
- Do they import without crashing?
- Do the core WebSocket helpers exist?

As you complete W0-1, W0-3, you can extend EXPECTED_MODULES
and add more assertions.
"""

from __future__ import annotations

import importlib
import types
from typing import List

import pytest


# ---------------------------------------------------------------------------
# 1) WebSocket shim expectations (W0-1)
# ---------------------------------------------------------------------------

WEBSOCKET_SHIM = "scripts._socket_http_extended"

WEBSOCKET_REQUIRED_ATTRS = [
    "DEFAULT_SOCKET_OPTION",
    "recv_line",
    "send_bytes",
]


def import_optional_module(name: str) -> types.ModuleType:
    """
    Import a module and fail with a clearer error if it breaks.

    This is used both for the WebSocket shim and the other Week-0 shims.
    """
    try:
        return importlib.import_module(name)
    except Exception as exc:  # broad on purpose – we want to surface import failures
        raise AssertionError(f"Failed to import {name!r} during Week-0 check: {exc}") from exc


def test_websocket_shim_module_exists() -> None:
    """
    W0-1: The websocket HTTP shim must exist and be importable.
    """
    mod = import_optional_module(WEBSOCKET_SHIM)
    assert isinstance(mod, types.ModuleType)


@pytest.mark.parametrize("attr_name", WEBSOCKET_REQUIRED_ATTRS)
def test_websocket_shim_has_required_attributes(attr_name: str) -> None:
    """
    W0-1: The websocket shim must expose the core helpers we agreed on.
    """
    mod = import_optional_module(WEBSOCKET_SHIM)
    assert hasattr(mod, attr_name), f"{WEBSOCKET_SHIM} is missing {attr_name!r}"


# ---------------------------------------------------------------------------
# 2) Core Week-0 shim modules that should import cleanly (W0-3 clusters)
#    NOTE: You can add/remove from this list as you implement shims.
# ---------------------------------------------------------------------------

EXPECTED_MODULES: List[str] = [
    # NumPy / numeric cluster (W0-3A)
    "scripts._pocketfft",
    "scripts._polybase",
    "scripts._spinners",
    "scripts._random",
    # Network / file helpers (W0-3B)
    "scripts.response",
    "scripts._util",
    "scripts._serialization",
    # Trio-like async cluster (W0-3C)
    "scripts._print_versions",
    "scripts._resources",
    "scripts._tasks",
    "scripts._streams",
    "scripts._streams_2",
    "scripts._subprocess",
    "scripts._subprocesses",
    "scripts._subprocesses_2",
    "scripts._sync",
    "scripts._sockets_2",
    # Add more here as you finish shims
]


@pytest.mark.parametrize("mod_name", EXPECTED_MODULES)
def test_week0_cluster_modules_import(mod_name: str) -> None:
    """
    W0-3: All key shim modules for Week-0 should import without raising.

    If this fails, it means Week-0 is NOT complete yet.
    Use the failure message to see which module still needs a shim.
    """
    import_optional_module(mod_name)
