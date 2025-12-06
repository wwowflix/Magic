from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any
import json


OUTPUT = Path(__file__).resolve().parents[1] / "outputs" / "week1_reporting_output.json"


@dataclass
class RunReport:
    total_flows: int
    successful: int
    failed: int
    meta: Dict[str, Any]


def build_report(
    total_flows: int = 5,
    successful: int = 4,
    failed: int = 1,
) -> RunReport:
    """
    Week1 reporting MVP:

    Just creates a small summary object.
    """
    return RunReport(
        total_flows=total_flows,
        successful=successful,
        failed=failed,
        meta={"mvp": True, "label": "week1-demo"},
    )


def save_report(report: RunReport) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")


def main() -> None:
    report = build_report()
    save_report(report)
    print(
        f"[W1-REPORT] OK: {report.successful}/{report.total_flows} "
        f"flows successful (failed={report.failed})"
    )


if __name__ == "__main__":
    main()
