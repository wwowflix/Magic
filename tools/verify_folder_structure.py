#!/usr/bin/env python
"""
verify_folder_structure.py

Checks that MAGIC phase folders (phase0..phase17) and their module subfolders exist
and generates a simple TSV report.

Usage:
    python tools/verify_folder_structure.py --root E:\MAGIC\scripts
"""

from __future__ import annotations
import argparse
from pathlib import Path
import sys

EXPECTED_PHASE_COUNT = 18  # phase0 .. phase17

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "scripts"),
        help="Root scripts folder (default: <repo_root>/scripts)",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"[ERROR] Scripts root does not exist: {root}", file=sys.stderr)
        return 1

    outputs_dir = root.parents[0] / "outputs" / "reports"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    report_path = outputs_dir / "structure_report.tsv"

    phase_dirs = sorted([p for p in root.iterdir() if p.is_dir() and p.name.startswith("phase")])

    lines = []
    header = "phase\tphase_path\tmodule_count\tscript_count"
    lines.append(header)

    for phase_dir in phase_dirs:
        modules = [m for m in phase_dir.iterdir() if m.is_dir()]
        module_count = len(modules)
        script_count = 0
        for m in modules:
            script_count += len(list(m.glob("*.py")))
        lines.append(f"{phase_dir.name}\t{phase_dir}\t{module_count}\t{script_count}")

    with report_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Wrote structure report to: {report_path}")

    # Basic sanity check on phase count (not fatal)
    if len(phase_dirs) != EXPECTED_PHASE_COUNT:
        print(
            f"[WARN] Expected {EXPECTED_PHASE_COUNT} phase folders, "
            f"found {len(phase_dirs)} under {root}",
            file=sys.stderr,
        )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
