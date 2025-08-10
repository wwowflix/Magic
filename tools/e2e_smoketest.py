#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAGIC – E2E Smoketest (Phase handoff + logs presence, FAIL-aware)
- Robust phase detection:
  * Accepts Phase/PhaseNumber/phase_id, values like "11", "11.0", "phase11"
  * Falls back to deriving phase from Filename or Folder if missing
- Only requires log folders for modules that have FAIL rows
- For FAIL rows, checks a matching .log exists (by script basename)
- Emits a JSON report; exits non-zero on critical gaps
"""

import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

PHASE_COL_CANDS = [
    "phase", "phasenumber", "phase_number", "phaseid", "phase_id", "phase num", "phase no"
]
STATUS_COL_CANDS = ["status", "result", "outcome"]
FILE_COL_CANDS = ["filename", "finalfilename", "script", "name", "file"]
FOLDER_COL_CANDS = ["folder", "path", "location"]

def pick_col(row_keys: List[str], candidates: List[str]) -> Optional[str]:
    lut = {k.lower(): k for k in row_keys}
    for c in candidates:
        if c.lower() in lut:
            return lut[c.lower()]
    return None

def parse_phase_value(val) -> Optional[int]:
    if val is None:
        return None
    s = str(val).strip()
    if s.isdigit():
        try:
            return int(s)
        except Exception:
            return None
    m = re.search(r'(\d+)', s)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None

def derive_phase(filename: str = "", folder: str = "") -> Optional[int]:
    if filename:
        m = re.search(r'\b(\d{1,2})[A-Z][_\-]', filename)
        if m:
            return int(m.group(1))
    if folder:
        m = re.search(r'phase[_/\\\-\s]?(\d{1,2})', folder, flags=re.I)
        if m:
            return int(m.group(1))
    return None

def derive_module(filename: str = "", folder: str = "") -> str:
    if filename:
        m = re.search(r'\b(\d{1,2})([A-Z])[_\-]', filename)
        if m:
            return m.group(2).upper()
    if folder:
        m = re.search(r'module[_/\\\-\s]?([A-Z])', folder, flags=re.I)
        if m:
            return m.group(1).upper()
    return "UNK"

def normalize_status(val: str) -> str:
    if val is None:
        return "OTHER"
    v = str(val).strip().upper()
    if v in {"PASS", "SUCCESS", "OK", "DONE", "PASSED", "EXECUTED SUCCESSFULLY", "COMPLETED", "GREEN"}:
        return "PASS"
    if v in {"FAIL", "FAILED", "ERROR", "ERR", "RED"} or "FAIL" in v or "ERROR" in v:
        return "FAIL"
    if v in {"MISSING", "NOT_FOUND", "ABSENT", "NOT FOUND"}:
        return "MISSING"
    if "SKIP" in v:
        return "SKIPPED"
    return v or "OTHER"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default="outputs/summaries/phase_master_summary.tsv")
    ap.add_argument("--logs_root", default="outputs/logs")
    ap.add_argument("--phase", type=int, default=11)
    ap.add_argument("--report", default="outputs/summaries/e2e_report.json")
    args = ap.parse_args()

    if not os.path.isfile(args.summary):
        print(f"ERROR: Summary TSV not found: {args.summary}", file=sys.stderr)
        return 2

    # Load TSV
    rows = []
    with open(args.summary, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            rows.append(r)

    if not rows:
        print("ERROR: Summary TSV is empty.", file=sys.stderr)
        return 2

    header = list(rows[0].keys())
    col_phase  = pick_col(header, PHASE_COL_CANDS)
    col_status = pick_col(header, STATUS_COL_CANDS)
    col_file   = pick_col(header, FILE_COL_CANDS)
    col_folder = pick_col(header, FOLDER_COL_CANDS)

    # Normalize rows
    norm = []
    for r in rows:
        phase_val = parse_phase_value(r.get(col_phase)) if col_phase else None
        if phase_val is None:
            phase_val = derive_phase(r.get(col_file, ""), r.get(col_folder, ""))
        module_val = derive_module(r.get(col_file, ""), r.get(col_folder, ""))
        status_val = normalize_status(r.get(col_status)) if col_status else "OTHER"
        norm.append({
            "phase": phase_val,
            "module": module_val,
            "status": status_val,
            "file": r.get(col_file, "") if col_file else "",
            "folder": r.get(col_folder, "") if col_folder else "",
            "raw": r,
        })

    # Distribution (debug aid)
    phase_counts = Counter([n["phase"] for n in norm if n["phase"] is not None])

    # Filter
    phase_rows = [n for n in norm if n["phase"] == args.phase]
    if not phase_rows:
        print(f"ERROR: No rows found for Phase {args.phase}.", file=sys.stderr)
        if phase_counts:
            top = ", ".join([f"{k}:{v}" for k, v in sorted(phase_counts.items())])
            print(f"Hint: Detected phases present → {top}", file=sys.stderr)
        else:
            print("Hint: No phase could be derived. Check headers or filename/folder patterns.", file=sys.stderr)
        return 1

    statuses = Counter([n["status"] for n in phase_rows])

    # Group by module
    mod_rows = defaultdict(list)
    for n in phase_rows:
        mod_rows[n["module"]].append(n)

    # Only modules with FAIL rows require log folders
    modules_need_logs = sorted({m for m, items in mod_rows.items() if any(n["status"] == "FAIL" for n in items)})

    missing_log_folders = []
    for mod in modules_need_logs:
        expected = os.path.join(args.logs_root, f"phase{args.phase}_module_{mod}")
        if not os.path.isdir(expected):
            missing_log_folders.append(expected)

    # For FAIL rows, ensure a log exists
    missing_logs = []
    for n in phase_rows:
        if n["status"] != "FAIL":
            continue
        mod = n["module"]
        base = os.path.splitext(os.path.basename(n["file"]))[0] if n["file"] else None
        log_dir = os.path.join(args.logs_root, f"phase{args.phase}_module_{mod}")
        found = False
        if base and os.path.isdir(log_dir):
            for name in os.listdir(log_dir):
                if name.endswith(".log") and base in name:
                    found = True
                    break
        if not found:
            missing_logs.append({"module": mod, "script": base or "(unknown)", "log_dir": log_dir})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "summary_path": os.path.abspath(args.summary),
        "logs_root": os.path.abspath(args.logs_root),
        "totals": dict(statuses),
        "modules_seen": sorted(mod_rows.keys()),
        "modules_need_logs": modules_need_logs,
        "phase_distribution_detected": dict(phase_counts),
        "missing_log_folders": missing_log_folders,
        "missing_logs_for_fail_rows": missing_logs,
        "ok": len(phase_rows) > 0 and not missing_log_folders and not missing_logs,
    }

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if not report["ok"]:
        print("E2E: FAIL. See report for details:", args.report, file=sys.stderr)
        return 1

    print("E2E: OK. Report:", args.report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
