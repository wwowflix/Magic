#!/usr/bin/env python3
"""
0A_sorter_READY.py
Moves files from inbox/ -> scripts/phase{NN}/module_{Letter}/
Pattern: NN<L>_anything_READY.py   e.g., 03C_demo_READY.py
"""

import argparse, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "inbox"
SCRIPTS = ROOT / "scripts"

PAT = re.compile(r"^(?P<phase>\d{2})(?P<mod>[A-Z])_.*_READY\.py$")

def target_for(name: str) -> Path | None:
    m = PAT.match(name)
    if not m:
        return None
    phase = int(m.group("phase"))
    mod = m.group("mod")
    dest = SCRIPTS / f"phase{phase}" / f"module_{mod}"
    dest.mkdir(parents=True, exist_ok=True)
    return dest / name

def main():
    ap = argparse.ArgumentParser(description="Move *_READY.py from inbox to scripts/* by phase/module.")
    ap.add_argument("--dry-run", action="store_true", help="Show moves but don't perform them")
    ap.add_argument("--verbose", action="store_true", help="Verbose output")
    args = ap.parse_args()

    if not INBOX.exists():
        print(f"inbox folder not found: {INBOX}")
        return 2

    moved = 0
    for p in sorted(INBOX.glob("*_READY.py")):
        tgt = target_for(p.name)
        if not tgt:
            if args.verbose:
                print(f"skip (name not matching convention): {p.name}")
            continue
        if args.verbose:
            print(f"{p}  ->  {tgt}")
        if not args.dry_run:
            shutil.move(str(p), str(tgt))
        moved += 1
    if args.verbose:
        print(f"done, files moved: {moved}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
