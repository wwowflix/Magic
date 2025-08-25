#!/usr/bin/env python3
"""
Self-Healing Runner v5 â€“ Parallel Execution
"""
import argparse
import subprocess
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed


def parse_args():
    parser = argparse.ArgumentParser(description="Self-Healing Runner v5 - Parallel")
    parser.add_argument("--manifest", required=True, help="Path to JSON manifest")
    parser.add_argument(
        "--phases", nargs="+", type=int, help="List of phase numbers to run"
    )
    parser.add_argument(
        "--modules", nargs="+", help="List of module identifiers to run"
    )
    parser.add_argument(
        "--max-workers", type=int, default=4, help="Max parallel workers"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List scripts without running"
    )
    return parser.parse_args()


def load_manifest(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading manifest: {e}")
        sys.exit(1)


def filter_manifest(manifest, phases, modules):
    filtered = []
    for entry in manifest:
        phase = entry.get("Phase") or entry.get("PhaseNumber")
        module = entry.get("Module")
        path = (
            entry.get("Path") or entry.get("FinalFilename") or entry.get("ScriptPath")
        )
        if not path:
            continue
        try:
            phase = int(phase)
        except (TypeError, ValueError):
            continue
        if phases and phase not in phases:
            continue
        if modules and module not in modules:
            continue
        filtered.append(path)
    return filtered


def run_script(script):
    if not os.path.isfile(script):
        return (script, "NOT FOUND", "", "")
    proc = subprocess.Popen(
        ["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = proc.communicate()
    status = "PASS" if proc.returncode == 0 else "FAIL"
    base = os.path.splitext(os.path.basename(script))[0]
    log_dir = os.path.join("outputs", "logs", base)
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "stdout.log"), "w", encoding="utf-8") as f:
        f.write(stdout)
    with open(os.path.join(log_dir, "stderr.log"), "w", encoding="utf-8") as f:
        f.write(stderr)
    with open(os.path.join(log_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(status)
    return (script, status, stdout, stderr)


def main():
    args = parse_args()
    manifest = load_manifest(args.manifest)
    scripts = filter_manifest(manifest, args.phases, args.modules)
    if not scripts:
        print("No matching scripts found.")
        return
    print(f"ðŸŒ€ Executing {len(scripts)} scripts with {args.max_workers} workers...")
    if args.dry_run:
        for s in scripts:
            print(s)
        return
    results = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(run_script, s): s for s in scripts}
        for future in as_completed(futures):
            script, status, _, _ = future.result()
            print(f"{status} â€” {script}")
            results.append(status)
    passed = results.count("PASS")
    failed = results.count("FAIL")
    not_found = results.count("NOT FOUND")
    print(
        f"\n=== SUMMARY ===\nTotal: {len(results)} | Passed: {passed} | Failed: {failed} | Missing: {not_found}"
    )


if __name__ == "__main__":
    main()
