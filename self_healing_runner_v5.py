# self_healing_runner_v5.py
from __future__ import annotations
import argparse
import json
import os
import sys
import subprocess
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = os.path.abspath(os.path.dirname(__file__))


def load_manifest(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Manifest JSON must be a list")
    return data


def normalize_entry(e: Dict[str, Any]) -> Tuple[int, str, str]:
    # Accept PhaseNumber or Phase
    if "PhaseNumber" in e:
        phase = int(e["PhaseNumber"])
    elif "Phase" in e:
        phase = int(e["Phase"])
    else:
        raise ValueError("missing Phase/PhaseNumber")

    # Normalize module to lowercase
    mod_raw = e.get("Module")
    if mod_raw is None or str(mod_raw).strip() == "":
        raise ValueError("missing Module")
    module = str(mod_raw).strip().lower()

    # Final filename may be a filename or a scripts/... path
    final = e.get("FinalFilename")
    if final is None or str(final).strip() == "":
        raise ValueError("missing FinalFilename")
    final = str(final).replace("\\", "/").strip()
    if final.startswith("scripts/"):
        rel = final
    else:
        rel = f"scripts/phase{phase}/module_{module}/{final}"
    return phase, module, rel


def filter_manifest(
    entries: Iterable[Dict[str, Any]],
    wanted_phases: Optional[Sequence[int]] = None,
    wanted_modules: Optional[Sequence[str]] = None,
) -> List[Dict[str, Any]]:
    phases = set(map(int, wanted_phases or []))
    modules = set(m.lower() for m in (wanted_modules or []))
    selected: List[Dict[str, Any]] = []
    reasons: List[str] = []

    for e in entries:
        try:
            phase, module, rel = normalize_entry(e)
        except Exception as ex:
            reasons.append(f"bad-entry: {ex} | entry={e}")
            continue
        if phases and phase not in phases:
            reasons.append(f"filtered: phase {phase} not in {sorted(phases)}")
            continue
        if modules and module not in modules:
            reasons.append(f"filtered: module '{module}' not in {sorted(modules)}")
            continue
        selected.append({"phase": phase, "module": module, "rel": rel})

    if not selected:
        print("No matching entries found in manifest. Nothing to run.")
        for r in reasons[:20]:
            print("  reason:", r)
        if len(reasons) > 20:
            print(f"  ... and {len(reasons)-20} more")
    return selected


def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def write_module_summary(
    phase: int, module: str, rows: List[Tuple[str, str]], summary_dir: str
) -> str:
    ensure_dir(summary_dir)
    out = os.path.join(summary_dir, f"phase{phase}_module_{module.upper()}_summary.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("Script\tStatus\n")
        for script_name, status in rows:
            f.write(f"{script_name}\t{status}\n")
    return out


def run_script(rel_path: str) -> int:
    abs_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(abs_path):
        # Treat missing as FAIL (runner should surface this clearly)
        print(f"[MISS] {rel_path} (file not found)")
        return 1
    # Use the current interpreter; inherit env; capture output to console
    proc = subprocess.run([sys.executable, abs_path])
    return proc.returncode


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Patch 2: Normalize + filter manifest entries with diagnostics"
    )
    ap.add_argument("--manifest", required=True, help="Path to phase_manifest.json")
    ap.add_argument(
        "--phases", nargs="+", type=int, help="Phases to include (e.g., 11 99)"
    )
    ap.add_argument(
        "--modules", nargs="+", help="Modules to include (e.g., C D E or ZZ)"
    )
    ap.add_argument(
        "--list", action="store_true", help="Print selected entries and exit"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="Do not execute, only report"
    )
    ap.add_argument(
        "--summary-dir",
        default=os.path.join(ROOT, "outputs", "summaries"),
        help="Where to write TSV summaries",
    )
    args = ap.parse_args(argv)

    try:
        entries = load_manifest(args.manifest)
    except Exception as ex:
        print(f"Error loading manifest: {ex}")
        return 2

    selected = filter_manifest(entries, args.phases, args.modules)
    print(f"Selected count: {len(selected)}")
    if not selected:
        return 0

    if args.list:
        for s in selected[:200]:
            print(f"- phase={s['phase']} module={s['module']} rel={s['rel']}")
        if len(selected) > 200:
            print(f"... and {len(selected)-200} more")
        return 0

    if args.dry_run:
        print("Dry-run: would execute the selected scripts above.")
        return 0

    # Group by (phase, module) and execute
    grouped: Dict[Tuple[int, str], List[Dict[str, Any]]] = defaultdict(list)
    for s in selected:
        grouped[(s["phase"], s["module"])].append(s)

    for (phase, module), items in grouped.items():
        print(f"\n=== Running Phase {phase}, Module {module.upper()} ===")
        rows: List[Tuple[str, str]] = []
        for s in items:
            rel = s["rel"]
            name = os.path.basename(rel)
            print(f"-> {rel}")
            code = run_script(rel)
            rows.append((name, "PASS" if code == 0 else "FAIL"))
        out = write_module_summary(phase, module, rows, args.summary_dir)
        print(f"Wrote summary: {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
