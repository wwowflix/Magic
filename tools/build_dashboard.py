"""
Minimal MAGIC dashboard builder (clean version)
- reads a TSV
- prints summary
- safe for pytest + coverage
"""
from __future__ import annotations

import pathlib
import sys
import csv


def load_rows(tsv_path: pathlib.Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with tsv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows


def summarize(rows: list[dict[str, str]]) -> dict[str, int]:
    out: dict[str, int] = {"PASS": 0, "FAIL": 0, "OTHER": 0}
    for r in rows:
        status = (r.get("Status") or "").upper()
        if status == "PASS":
            out["PASS"] += 1
        elif status == "FAIL":
            out["FAIL"] += 1
        else:
            out["OTHER"] += 1
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        # default for tests
        tsv_path = pathlib.Path("outputs/reports/phase_master_summary.tsv")
    else:
        tsv_path = pathlib.Path(argv[0])

    if not tsv_path.exists():
        # graceful for tests
        print(f"[dashboard] {tsv_path} not found, nothing to do.")
        return 0

    rows = load_rows(tsv_path)
    summary = summarize(rows)
    print("[dashboard] PASS:", summary["PASS"])
    print("[dashboard] FAIL:", summary["FAIL"])
    print("[dashboard] OTHER:", summary["OTHER"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
