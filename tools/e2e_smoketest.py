from pathlib import Path
import argparse
import csv
import json
import sys


def _iter_rows(tsv: Path):
    with tsv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            yield row


def _expected_log_path(row: dict[str, str], logs_root: Path) -> Path:
    # Filename like 11B_bar.py -> phase dir "phase11_module_B", log "11B_bar.log"
    fname = str(row.get("Filename", "")).strip()
    phase = str(row.get("Phase", "")).strip()
    module_letter = ""
    if len(fname) >= 3 and fname[:2].isdigit():
        module_letter = fname[2]
    subdir = f"phase{phase}_module_{module_letter}" if phase and module_letter else f"phase{phase}"
    logname = fname.replace(".py", ".log") if fname else "unknown.log"
    return logs_root / subdir / logname


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--summary", type=Path, required=True, help="Path to phase_master_summary.tsv")
    # accept both styles
    p.add_argument(
        "--logs-root",
        "--logs_root",
        dest="logs_root",
        type=Path,
        default=Path("outputs/logs"),
    )
    p.add_argument("--phase", type=str, default=None, help="Filter by Phase, e.g. 11")
    p.add_argument("--report", type=Path, default=Path("e2e_report.json"))
    args = p.parse_args(argv)

    rows = list(_iter_rows(args.summary))
    if args.phase:
        want = args.phase.strip()
        rows = [r for r in rows if str(r.get("Phase", "")).strip() == want]

    pass_count = 0
    fail_count = 0
    missing_logs: list[dict[str, str]] = []

    for r in rows:
        status = str(r.get("Status", "")).strip().upper()
        if status == "PASS":
            pass_count += 1
        elif status == "FAIL":
            fail_count += 1
            exp = _expected_log_path(r, args.logs_root)
            if not exp.exists():
                missing_logs.append({"Filename": r.get("Filename", ""), "expected_log": str(exp)})

    overall_ok = len(missing_logs) == 0
    phase_field = int(args.phase) if (args.phase and args.phase.isdigit()) else args.phase
    totals = {"PASS": pass_count, "FAIL": fail_count, "TOTAL": pass_count + fail_count}

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(
            {
                "ok": overall_ok,
                "phase": phase_field,
                "totals": totals,
                "missing_logs": missing_logs,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Non-zero only if summary had no rows after filtering
    if not rows:
        print("No rows matched the filter/summary.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
