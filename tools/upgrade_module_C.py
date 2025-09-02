# tools/upgrade_module_C.py
import os, sys, json, hashlib, shutil, argparse, datetime, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "outputs" / "module_C"
SRC  = ROOT / "scripts" / "phase11" / "module_C"
SRC.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

# --- Script 1: 11C_corruption_recovery_agent_READY.py ---
corruption = r'''#!/usr/bin/env python3
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
'''

# --- Script 2: 11C_fail_safe_backup_system_READY.py ---
backup = r'''#!/usr/bin/env python3
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
'''

# --- Script 3: 11C_script_integrity_checker_READY.py ---
integrity = r'''#!/usr/bin/env python3
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
'''

# --- Script 4: 11C_placeholder_READY.py (heartbeat/no-op with artifacts) ---
heartbeat = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, datetime
from pathlib import Path

def main():
    out = Path("outputs/module_C/heartbeat")
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "module": "C",
        "name": "11C_placeholder_heartbeat",
        "utc": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "OK"
    }
    with open(out / "heartbeat.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {out/'heartbeat.json'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

# --- Script 5: phase11_module_C_placeholder_READY.py (aggregates results) ---
aggregate = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, csv
from pathlib import Path

def main():
    out = Path("outputs/module_C/aggregate"); out.mkdir(parents=True, exist_ok=True)
    srcs = [
        Path("outputs/module_C/integrity/integrity.csv"),
        Path("outputs/module_C/corruption_recovery/recovery_report.tsv"),
    ]
    summary = out / "module_C_summary.tsv"
    rows = [("source","line")]
    for s in srcs:
        if not s.exists(): 
            rows.append((str(s), "NOT_FOUND"))
            continue
        with open(s, "r", encoding="utf-8", newline="") as f:
            for line in f:
                rows.append((str(s), line.strip()))

    with open(summary, "w", encoding="utf-8", newline="") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")

    print(f"Aggregated {len(rows)-1} lines into {summary}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

FILES = {
    SRC / "11C_corruption_recovery_agent_READY.py": corruption,
    SRC / "11C_fail_safe_backup_system_READY.py":   backup,
    SRC / "11C_script_integrity_checker_READY.py":  integrity,
    SRC / "11C_placeholder_READY.py":               heartbeat,
    SRC / "phase11_module_C_placeholder_READY.py":  aggregate,
}

def main():
    for path, content in FILES.items():
        write(path, content)
        print(f"Wrote {path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
