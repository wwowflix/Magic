#!/usr/bin/env python3
import os
import sys
import csv
import ast

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
tsv_in  = sys.argv[1]
tsv_out = sys.argv[2]

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ------------------------
# AGGRESSIVE EXCLUDES v2
# ------------------------
EXCLUDE_DIRS = (
    "scripts/phase00/INBOX/",
    "scripts/phase00/INBOX_CLONES/",
    "scripts/phase00/QUARANTINE/",
    "scripts/phase00/_imports/",
    "scripts/phase00/tmp/",
    "scripts/demo/",
    "scripts/examples/",
    "scripts/tests/",
    "scripts/bench/",
    "scripts/samples/",
)

EXCLUDE_SUFFIXES = (
    # your cloned / double-suffixed junk
    "_C5C59570_C5C59570.py",
    "_3D0444B9_3D0444B9.py",
    "_E8031571_E8031571.py",
    "_EBF97484_EBF97484.py",
    "_99E961C3_99E961C3.py",
    # generic tmp / scrap names
    ".tmp.py",
    ".broken.py",
)

# sometimes these are “python but not really”
EXCLUDE_PREFIXES = (
    "scripts/phase00/INBOX/__MACOSX/",
    "scripts/phase00/INBOX/~$",
)

def is_excluded(path: str) -> bool:
    if any(path.startswith(p) for p in EXCLUDE_DIRS):
        return True
    if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    if any(path.endswith(sfx) for sfx in EXCLUDE_SUFFIXES):
        return True
    return False

def should_check(path: str) -> bool:
    # must be python under scripts/
    if not (path.startswith("scripts/") and path.endswith(".py")):
        return False
    # ignore tests
    base = os.path.basename(path)
    if base.startswith("test_") or base.endswith("_test.py"):
        return False
    if is_excluded(path):
        return False
    return True

def ast_ok(fs_path: str) -> bool:
    try:
        with open(fs_path, "r", encoding="utf-8", errors="replace") as fh:
            src = fh.read()
        ast.parse(src, filename=fs_path)
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
        if is_excluded(path):
            status = "WARN"
        elif should_check(path):
            fs_path = os.path.join(ROOT, path.replace("/", os.sep))
            status  = "PASS" if ast_ok(fs_path) else "FAIL"
        r["status"] = status
        rows.append(r)

with open(tsv_out, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, fieldnames=headers, delimiter="\t")
    wr.writeheader(); wr.writerows(rows)

fails = sum(1 for r in rows if r.get("status") == "FAIL")
print(f"MARK_OK\t{tsv_out}\t{fails} FAILs")
