#!/usr/bin/env python3
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

LOG_FOLDER_RE = re.compile(r"scripts/(phase\d+)/(module_[^/]+)/", re.IGNORECASE)


def _derive_log_path(logs_root: Path, folder_field: str, filename: str) -> Path:
    """
    Given Folder like 'scripts/phase11/module_B/' and Filename like '11B_bar.py',
    return logs_root/phase11_module_B/11B_bar.log
    """
    m = LOG_FOLDER_RE.search(folder_field.replace("\\", "/"))
    if not m:
        # fallback: throw into logs_root (still deterministic)
        log_name = filename.replace(".py", ".log")
        return logs_root / log_name
    phase_part, module_part = m.group(1), m.group(2)
    log_dir = f"{phase_part}_{module_part}"
    log_name = filename.replace(".py", ".log")
    return logs_root / log_dir / log_name


def _read_rows(summary_path: Path) -> List[Dict[str, str]]:
    with summary_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [dict(row) for row in reader]


def _filter_rows(rows: List[Dict[str, str]], phase: Optional[int]) -> List[Dict[str, str]]:
    if phase is None:
        return rows
    return [r for r in rows if str(r.get("Phase", "")).strip() == str(phase)]


def _summarize(
    rows: List[Dict[str, str]], logs_root: Path
) -> Tuple[Dict[str, int], list[dict[str, str]], bool]:
    totals: dict[str, int] = Counter()
    checked: list[dict[str, str]] = []
    ok = True

    for r in rows:
        status = str(r.get("Status", "")).strip()
        filename = str(r.get("Filename", "")).strip()
        folder = str(r.get("Folder", "")).strip()
        if not status:
            continue

        totals[status] += 1

        entry = {
            "filename": filename,
            "status": status,
            "phase": r.get("Phase", ""),
            "folder": folder,
        }

        if status.upper() == "FAIL":
            log_path = _derive_log_path(logs_root, folder, filename)
            found = log_path.exists()
            entry["log_found"] = found  # type: ignore[assignment]
            entry["log_path"] = str(log_path)
            if not found:
                ok = False  # type: ignore[assignment]

        checked.append(entry)

    # if there were simply no rows to check, that's OK
    return dict(totals), checked, ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="E2E smoketest for MAGIC runner outputs")
    ap.add_argument("--summary", required=True, help="Path to phase_master_summary.tsv")
    ap.add_argument("--logs_root", required=True, help="Root of outputs/logs")
    ap.add_argument("--report", required=True, help="Where to write JSON report")
    # ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ make --phase optional; aggregate if omitted
    ap.add_argument(
        "--phase",
        type=int,
        default=None,
        help="Phase number to check; omit to aggregate all",
    )
    ns = ap.parse_args(argv)

    summary_path = Path(ns.summary)
    logs_root = Path(ns.logs_root)
    report_path = Path(ns.report)

    if not summary_path.exists():
        # Write a small report with ok=False so callers can read diagnostics
        payload = {
            "ok": False,
            "error": "summary_not_found",
            "summary": str(summary_path),
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    rows = _read_rows(summary_path)
    rows = _filter_rows(rows, ns.phase)
    totals, checked, ok = _summarize(rows, logs_root)

    payload = {
        "ok": ok,
        "phase": (ns.phase if ns.phase is not None else "all"),
        "totals": totals,
        "checked": checked,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
