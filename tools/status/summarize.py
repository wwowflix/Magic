#!/usr/bin/env python3
import csv  # noqa: I001
import sys
import os
import glob

args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
inp = args.get("--in")
outp = args.get("--out")
if not inp:
    files = sorted(glob.glob("outputs/reports/magic_full_status_scan_*.tsv"))
    if not files:
        print("ERR\tno_scan_input")
        sys.exit(2)
    inp = files[-1]
if not outp:
    outp = "outputs/reports/status_live_latest.tsv"
counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
total = 0
with open(inp, encoding="utf-8") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    for r in rd:
        s = r["status"].strip().upper()
        counts[s] = counts.get(s, 0) + 1
        total += 1
pct = round((counts["PASS"] / total * 100), 2) if total else 0.0
os.makedirs(os.path.dirname(outp), exist_ok=True)
with open(outp, "w", encoding="utf-8", newline="") as fh:
    wr = csv.writer(fh, delimiter="\t")
    wr.writerow(["Metric", "Value"])
    wr.writerow(["Total files", total])
    wr.writerow(["PASS", counts["PASS"]])
    wr.writerow(["WARN", counts["WARN"]])
    wr.writerow(["FAIL", counts["FAIL"]])
    wr.writerow(["%PASS", pct])
print(f"SUM_OK\t{outp}\t{pct}")
