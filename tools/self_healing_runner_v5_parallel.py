#!/usr/bin/env python3
"""
Self-Healing Runner v5 (Parallel Edition)

Usage:
  python self_healing_runner_v5_parallel.py \
    --manifest phase_manifest.json \
    [--phases 1 2 3] \
    [--modules A B] \
    [--dry-run] \
    [--max-workers 4]
"""
import argparse
import subprocess
import json
import os
import sys
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

def parse_args():
    parser = argparse.ArgumentParser(description="Self-Healing Runner v5 Parallel")
    parser.add_argument('-m', '--manifest', required=True,
                        help='Path to JSON manifest file')
    parser.add_argument('--phases', nargs='+', type=int,
                        help='List of phase numbers to run')
    parser.add_argument('--modules', nargs='+',
                        help='List of module identifiers to run')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print scripts without executing')
    parser.add_argument('--max-workers', type=int, default=4,
                        help='Max parallel workers (default: 4)')
    return parser.parse_args()

def load_manifest(path):
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading manifest: {e}")
        sys.exit(1)

def filter_manifest(manifest, phases, modules):
    filtered = []
    for entry in manifest:
        entry_phase = entry.get('Phase') or entry.get('PhaseNumber') or entry.get('phase')
        entry_module = entry.get('Module') or entry.get('module')
        try:
            entry_phase_int = int(entry_phase)
        except:
            continue
        if phases and entry_phase_int not in phases:
            continue
        if modules and entry_module not in modules:
            continue
        script_path = entry.get('Path') or entry.get('ScriptPath') or entry.get('FinalFilename') or entry.get('filename')
        if not script_path:
            continue
        filtered.append(script_path)
    return filtered

def execute_script(script):
    if not os.path.isfile(script):
        return (script, 'NOT_FOUND', '', f'Script not found: {script}')
    proc = subprocess.Popen(
        ['python', script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate()
    status = 'PASS' if proc.returncode == 0 else 'FAIL'
    return (script, status, out, err)

def save_logs(script, status, out, err):
    base = os.path.splitext(os.path.basename(script))[0]
    log_dir = os.path.join('outputs', 'logs', base)
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'stdout.log'), 'w', encoding='utf-8') as f:
        f.write(out)
    with open(os.path.join(log_dir, 'stderr.log'), 'w', encoding='utf-8') as f:
        f.write(err)
    with open(os.path.join(log_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write(status)

def run_scripts_parallel(scripts, dry_run, max_workers):
    results = []
    if dry_run:
        for script in scripts:
            print(f"[DRY RUN] Would run: {script}")
        return
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(execute_script, script): script for script in scripts}
        for future in as_completed(futures):
            script = futures[future]
            try:
                script, status, out, err = future.result()
                print(f"▶ {script} => {status}")
                save_logs(script, status, out, err)
                results.append((script, status))
            except Exception as e:
                print(f"ERROR running {script}: {e}")
                results.append((script, 'ERROR'))
    return results

def main():
    args = parse_args()
    manifest = load_manifest(args.manifest)
    scripts = filter_manifest(manifest, args.phases, args.modules)
    if not scripts:
        print("No matching entries found in manifest. Nothing to run.")
        sys.exit(0)
    print(f"🔹 Starting Parallel Self-Healing Runner on {len(scripts)} scripts...")
    results = run_scripts_parallel(scripts, args.dry_run, args.max_workers)
    if results:
        passes = sum(1 for _, status in results if status == 'PASS')
        fails = sum(1 for _, status in results if status != 'PASS')
        print("\n=== SUMMARY ===")
        print(f"Total scripts: {len(results)}")
        print(f"Passed: {passes}")
        print(f"Failed: {fails}")
        print("Logs saved to: outputs/logs")

if __name__ == '__main__':
    main()
