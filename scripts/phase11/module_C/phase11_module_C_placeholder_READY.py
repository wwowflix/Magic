#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, csv
from pathlib import Path

def main():
    out = Path("outputs/module_C/aggregate"); out.mkdir(parents=True, exist_ok=True)
    srcs = [
        Path("outputs/module_C/integrity/integrity.csv"),
        Path("outputs/module_C/corruption_recovery/recovery_report.tsv"),
    ]
    summary = out / "module_C_summary.tsv"
    rows = [("source","line")]
    for s in srcs:
        if not s.exists(): 
            rows.append((str(s), "NOT_FOUND"))
            continue
        with open(s, "r", encoding="utf-8", newline="") as f:
            for line in f:
                rows.append((str(s), line.strip()))

    with open(summary, "w", encoding="utf-8", newline="") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")

    print(f"Aggregated {len(rows)-1} lines into {summary}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
