from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from scripts.flow_manifest_builder import build_manifest

REPORT_PATH = Path("config") / "report_week1_summary.json"


def build_report() -> Dict[str, Any]:
    """
    Build a minimal Week-1 summary report based on the flow manifest.

    We call build_manifest() directly so tests do not depend on any
    specific JSON file being present on disk.
    """
    modules: List[Dict[str, Any]] = build_manifest()

    total = len(modules)
    by_category: Dict[str, int] = {}
    enabled_count = 0

    for item in modules:
        cat = str(item.get("category", "unknown"))
        by_category[cat] = by_category.get(cat, 0) + 1

        if bool(item.get("enabled", False)):
            enabled_count += 1

    report: Dict[str, Any] = {
        "total_modules": total,
        "enabled_modules": enabled_count,
        "by_category": by_category,
    }
    return report


def write_report(path: Path | None = None) -> tuple[Path, Dict[str, Any]]:
    """
    Write the report JSON to disk.

    Returns (path_written, report_dict).
    """
    target = Path(path) if path is not None else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    target.write_text(text, encoding="utf-8")
    return target, report


def main() -> None:
    path, report = write_report()
    print(f"[MAGIC] Week-1 report written to {path}")
    print(f"[MAGIC] total_modules={report.get('total_modules')}, "
          f"enabled_modules={report.get('enabled_modules')}")
    print(f"[MAGIC] by_category={report.get('by_category')}")


if __name__ == "__main__":
    main()
