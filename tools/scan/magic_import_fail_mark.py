#!/usr/bin/env python3
import os  # noqa: I001
import sys
import csv
import ast

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
tsv_in = sys.argv[1]
tsv_out = sys.argv[2]

if root not in sys.path:
    sys.path.insert(0, root)

EXCLUDE_DIRS = (
    "scripts/tests/",
    "scripts/examples/",
    "scripts/demo/",
    "scripts/bench/",
    "scripts/phase00/QUARANTINE/",
    "scripts/phase00/QUARANTINE/garbled/",
    "scripts/phase00/QUARANTINE/numpy_shadowed/",
)


def is_excluded(path: str) -> bool:
    return any(path.startswith(d) for d in EXCLUDE_DIRS)


def should_check(path: str) -> bool:
    if not (path.startswith("scripts/") and path.endswith(".py")):
        return False
    base = os.path.basename(path)
    if base.startswith("test_") or base.endswith("_test.py"):
        return False
    if is_excluded(path):
        return False
    return True


def ast_ok(file_path: str) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            src = fh.read()
        ast.parse(src, filename=file_path)
        return True
    except Exception:
        return False


rows, headers = [], None
with open(tsv_in, encoding="utf-8") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    headers = rd.fieldnames
    for r in rd:
        path = r["path"]
        status = r.get("status", "")
        fs_path = os.path.join(root, path.replace("/", os.sep))
        if is_excluded(path):
            status = "WARN"
        elif should_check(path):
            status = "PASS" if (os.path.isfile(fs_path) and ast_ok(fs_path)) else "FAIL"
        else:
            # not a checked script → never leave FAIL hanging
            status = "WARN"
        r["status"] = status
        rows.append(r)

with open(tsv_out, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, fieldnames=headers, delimiter="\t")
    wr.writeheader()
    wr.writerows(rows)

fails = sum(1 for r in rows if r.get("status") == "FAIL")
print(f"MARK_OK\t{tsv_out}\t{fails} FAILs")
