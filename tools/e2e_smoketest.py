#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="E2E smoketest for MAGIC runner outputs")
    p.add_argument("--summary", required=True, help="Path to phase_master_summary.tsv")
    # Support both spellings
    p.add_argument("--logs-root", dest="logs_root", help="Root dir containing phaseXX_module_* logs")
    p.add_argument("--logs_root", dest="logs_root", help=argparse.SUPPRESS)
    p.add_argument("--phase", help="Phase filter like '11'")
    p.add_argument("--report", help="Optional JSON report path")
    return p.parse_args(argv)

def expected_log_path(logs_root: Path, row: Dict[str, str], phase_override: Optional[str]) -> Path:
    filename = (row.get("Filename") or "").strip()
    folder = (row.get("Folder") or "").strip().rstrip("/\\")
    phase = (phase_override or (row.get("Phase") or "")).strip()

    # derive module name
    module_name = Path(folder).name or ""
    if not module_name.startswith("module_") and len(filename) >= 3 and filename[:2].isdigit():
        module_name = f"module_{filename[2]}"

    log_dir = logs_root / f"phase{phase}_{module_name}"
    log_file = Path(filename).stem + ".log"
    return log_dir / log_file

def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    summary_path = Path(args.summary)
    logs_root = Path(args.logs_root) if args.logs_root else Path("outputs/logs")
    phase_override = args.phase
    report_path = Path(args.report) if args.report else None

    missing: List[str] = []
    total_fail_rows = 0

    with summary_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for col in ("Filename", "Status", "Phase", "Folder"):
            if not reader.fieldnames or col not in reader.fieldnames:
                print(f"Missing column '{col}' in summary TSV", file=sys.stderr)
                return 2
        for row in reader:
            if phase_override and (row.get("Phase") or "").strip() != str(phase_override):
                continue
            if (row.get("Status") or "").strip().upper() != "FAIL":
                continue
            total_fail_rows += 1
            p = expected_log_path(logs_root, row, phase_override)
            if not p.exists():
                missing.append(str(p))

    out: Dict[str, object] = {"phase": phase_override or None,
                              "fail_rows": total_fail_rows,
                              "missing_logs": missing}

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    if missing:
        for m in missing:
            print(f"Missing log: {m}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())