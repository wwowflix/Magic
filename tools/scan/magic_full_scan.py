#!/usr/bin/env python3
import os  # noqa: I001
import csv
import datetime

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
scan_dirs = ["scripts", "tools"]
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
rows = []
for d in scan_dirs:
    base = os.path.join(root, d)
    if not os.path.isdir(base):
        continue
    for path, _, files in os.walk(base):
        for f in files:
            if not f.endswith(".py"):
                continue
            full = os.path.join(path, f)
            rel = os.path.relpath(full, root).replace("\\", "/")
            size = os.path.getsize(full)
            status = "PASS" if f.endswith("_READY.py") else "WARN"
            rows.append(
                {"path": rel, "size": size, "status": status, "timestamp": stamp}
            )
out_dir = os.path.join(root, "outputs", "reports")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, f"magic_full_status_scan_{stamp}.tsv")
with open(out_path, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(
        fh, fieldnames=["path", "size", "status", "timestamp"], delimiter="\t"
    )
    wr.writeheader()
    wr.writerows(rows)
print(f"SCAN_OK\t{out_path}\t{len(rows)}")
