from __future__ import annotations

import importlib
from scripts.error_flow_mvp import ErrorReport

CODES = ["ERR001", "ERR002", "ERR003"]


def test_generated_error_modules_import() -> None:
    for code in CODES:
        mod = importlib.import_module(f"scripts.generated.error_flow.error_{code}")
        assert hasattr(mod, "build_error_report")


def test_generated_error_reports() -> None:
    for code in CODES:
        mod = importlib.import_module(f"scripts.generated.error_flow.error_{code}")
        report = mod.build_error_report({"ok": True})
        assert isinstance(report, ErrorReport)
        assert "error_code" in report.context
        assert "severity" in report.context
