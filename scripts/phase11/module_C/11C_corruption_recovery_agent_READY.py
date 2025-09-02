#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, json, sys, shutil
from pathlib import Path

def is_corrupt_json(p: Path) -> bool:
    try:
        if not p.exists() or p.stat().st_size == 0:
            return True
        with open(p, "r", encoding="utf-8") as f:
            json.load(f)
        return False
    except Exception:
        return True

def main():
    ap = argparse.ArgumentParser(description="Corruption recovery agent")
    ap.add_argument("--scan", default="outputs", help="Folder to scan for *.json")
    ap.add_argument("--out", default="outputs/module_C/corruption_recovery", help="Output folder")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.scan)
    out  = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    report = out / "recovery_report.tsv"

    fixed = 0; checked = 0
    rows = [("file","status","action")]
    for p in root.rglob("*.json"):
        checked += 1
        corrupt = is_corrupt_json(p)
        action  = "none"
        if corrupt:
            bak = p.with_suffix(p.suffix + ".bak")
            if bak.exists() and bak.stat().st_size > 0:
                action = f"restore_from {bak.name}"
                if not args.dry_run:
                    shutil.copy2(bak, p)
                fixed += 1
            else:
                action = "no_backup_found"
        rows.append((str(p), "CORRUPT" if corrupt else "OK", action))

    with open(report, "w", encoding="utf-8", newline="") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")

    print(f"Checked={checked} Fixed={fixed} Report={report}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
