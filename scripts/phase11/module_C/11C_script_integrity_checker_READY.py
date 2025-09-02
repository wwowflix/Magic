#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, hashlib, os, sys, csv
from pathlib import Path

def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description="Script integrity checker")
    ap.add_argument("--root", default="scripts/phase11", help="Where scripts live")
    ap.add_argument("--out", default="outputs/module_C/integrity", help="Output dir")
    ap.add_argument("--min-bytes", type=int, default=300, help="Warn if file smaller than this")
    args = ap.parse_args()

    root = Path(args.root)
    out  = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    csvp = out / "integrity.csv"

    fields = ["path","bytes","sha256","status"]
    rows   = []
    for p in root.rglob("*.py"):
        try:
            size = p.stat().st_size
            status = "OK"
            if size < args.min_bytes:
                status = f"SMALL<{args.min_bytes}"
            rows.append({"path": str(p), "bytes": size, "sha256": sha256_of(p), "status": status})
        except Exception as e:
            rows.append({"path": str(p), "bytes": 0, "sha256": "", "status": f"ERROR:{e}"})

    with open(csvp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {csvp} ({len(rows)} rows)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
