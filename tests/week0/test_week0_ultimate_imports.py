from __future__ import annotations

import importlib
from typing import Dict, Iterable, Tuple
import pytest

CRITICAL_MODULES: Tuple[str, ...] = (
    "scripts._socket_http_extended",
    "scripts._iotools",
    "scripts._io_windows",
    "scripts._lxml",
    "scripts._lxml_2",
    "scripts._magics",
    "scripts._compat",
    "scripts._meta",
    "scripts._methods",
    "scripts._n_a_m_e",
)

SPECIAL_EXPECTATIONS: Dict[str, Tuple[str, ...]] = {
    "scripts._socket_http_extended": (
        "DEFAULT_SOCKET_OPTION",
        "recv_line",
        "send_bytes",
    ),
    "scripts._methods": (
        "_sum",
        "_prod",
        "_mean",
    ),
}

@pytest.mark.parametrize("module_name", CRITICAL_MODULES)
def test_import_critical_modules(module_name: str) -> None:
    mod = importlib.import_module(module_name)
    assert mod is not None, f"Import failed for {module_name!r}"

    expected_attrs: Iterable[str] = SPECIAL_EXPECTATIONS.get(module_name, ())
    for attr in expected_attrs:
        assert hasattr(mod, attr), f"{module_name!r} missing attribute {attr!r}"

def test_week0_summary_smoke() -> None:
    assert CRITICAL_MODULES, "CRITICAL_MODULES list is empty."
