from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import scripts.reporting_mvp as rep


def test_build_report_shape() -> None:
    report: Dict[str, Any] = rep.build_report()

    assert isinstance(report, dict)
    assert "total_modules" in report
    assert "enabled_modules" in report
    assert "by_category" in report

    assert isinstance(report["total_modules"], int)
    assert isinstance(report["enabled_modules"], int)
    assert isinstance(report["by_category"], dict)


def test_write_report_to_temp(tmp_path: Path) -> None:
    target = tmp_path / "report_week1_summary.json"

    written_path, report = rep.write_report(target)

    assert written_path == target
    assert written_path.exists()

    loaded = json.loads(written_path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    assert loaded.keys() >= {"total_modules", "enabled_modules", "by_category"}


def test_write_report_default_location() -> None:
    # Clean up any old report
    rep.REPORT_PATH.unlink(missing_ok=True)

    written_path, report = rep.write_report()

    assert written_path == rep.REPORT_PATH
    assert written_path.exists()
    data = json.loads(written_path.read_text(encoding="utf-8"))
    assert "total_modules" in data
