#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, shutil, sys, time
from pathlib import Path

INCLUDE = (".yml",".yaml",".json",".py",".env",".ini",".cfg")

def main():
    ap = argparse.ArgumentParser(description="Fail-safe backup system")
    ap.add_argument("--src", nargs="+", default=["config","scripts/common"], help="Folders to back up")
    ap.add_argument("--dest", default="backups", help="Backups root")
    ap.add_argument("--tag", default="", help="Optional tag for backup dir name")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ts   = time.strftime("%Y%m%d_%H%M%S")
    name = f"module_C_backup_{ts}{('-'+args.tag) if args.tag else ''}"
    dest = Path(args.dest) / name
    manifest = []

    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    for src in args.src:
        sp = Path(src)
        if not sp.exists():
            continue
        for p in sp.rglob("*"):
            if p.is_file() and p.suffix.lower() in INCLUDE:
                rel = p.relative_to(sp)
                dp  = dest / sp.name / rel
                if not args.dry_run:
                    dp.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dp)
                manifest.append((str(p), str(dp)))

    manpath = dest / "manifest.tsv"
    with open(manpath, "w", encoding="utf-8", newline="") as f:
        for srcp, dstp in manifest:
            f.write(f"{srcp}\t{dstp}\n")

    print(f"Backed up {len(manifest)} files to {dest} (manifest={manpath})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
