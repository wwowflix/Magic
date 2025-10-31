#!/usr/bin/env python3
# AST diag: produce a TSV with columns: path, status, diag_type, diag_msg
import os  # noqa: I001
import sys
import csv
import ast

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
tsv_in = sys.argv[1]
tsv_out = sys.argv[2]

if root not in sys.path:
    sys.path.insert(0, root)


def should_check(path: str) -> bool:
    if not (path.startswith("scripts/") and path.endswith(".py")):
        return False
    base = os.path.basename(path)
    if base.startswith("test_") or base.endswith("_test.py"):
        return False
    bad_dirs = (
        "scripts/tests/",
        "scripts/examples/",
        "scripts/demo/",
        "scripts/bench/",
    )
    if any(path.startswith(d) for d in bad_dirs):
        return False
    return True


rows, headers = [], None
with open(tsv_in, encoding="utf-8") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    headers = list(rd.fieldnames)
    if "diag_type" not in headers:
        headers += ["diag_type", "diag_msg"]
    for r in rd:
        path = r["path"]
        status = r.get("status", "")
        r["diag_type"] = ""
        r["diag_msg"] = ""
        if should_check(path):
            fs = os.path.join(root, path.replace("/", os.sep))
            try:
                with open(fs, "r", encoding="utf-8", errors="replace") as fh2:
                    src = fh2.read()
                ast.parse(src, filename=fs)
            except Exception as e:
                status = "FAIL"
                r["diag_type"] = e.__class__.__name__
                r["diag_msg"] = (
                    str(e).replace("\t", ").replace("\r", ").replace("\n", ")
                )
        r["status"] = status
        rows.append(r)

with open(tsv_out, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, fieldnames=headers, delimiter="\t")
    wr.writeheader()
    wr.writerows(rows)

fails = sum(1 for r in rows if r.get("status") == "FAIL")
print(f"DIAG_OK\t{tsv_out}\t{fails} FAILs")
