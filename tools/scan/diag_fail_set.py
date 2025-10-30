#!/usr/bin/env python3
import ast  # noqa: I001
import pathlib
import csv

fail_list = r".\outputs\reports\_fail_paths.txt"
out = r".\outputs\reports\magic_fail_diag_latest.tsv"

rows = []
for rel in pathlib.Path(fail_list).read_text().splitlines():
    p = pathlib.Path(rel)
    if not p.is_file():
        continue
    src = p.read_text(encoding="utf-8", errors="replace")
    try:
        ast.parse(src, filename=str(p))
        status = "OK"
        diag_type = ""
        diag_msg = ""
    except Exception as e:
        status = "FAIL"
        diag_type = type(e).__name__
        diag_msg = str(e).replace("\t", " ").replace("\n", " ")
    rows.append(
        {"path": rel, "status": status, "diag_type": diag_type, "diag_msg": diag_msg}
    )

with open(out, "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(
        fh, fieldnames=["path", "status", "diag_type", "diag_msg"], delimiter="\t"
    )
    wr.writeheader()
    wr.writerows(rows)

print(f"DIAG_OK {out} {sum(r['status']=='FAIL' for r in rows)} FAILs")
