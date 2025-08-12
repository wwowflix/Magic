#!/usr/bin/env python3
"""
Self-Healing Runner v5

Usage:
  python self_healing_runner_v5.py \
    --manifest phase_manifest.json \
    [--phases 1 2 3] \
    [--modules A B] \
    [--dry-run]

This script loads a JSON manifest of scripts, filters by phase and/or module,
executes each script, captures stdout/stderr, and writes per-script logs.
"""
import argparse
import subprocess
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Self-Healing Runner v5")
    parser.add_argument('-m', '--manifest', required=True,
                        help='Path to JSON manifest file')
    parser.add_argument('--phases', nargs='+', type=int,
                        help='List of phase numbers to run')
    parser.add_argument('--modules', nargs='+',
                        help='List of module identifiers to run')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print scripts without executing')
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
        # support multiple key names
        entry_phase = entry.get('Phase') or entry.get('PhaseNumber') or entry.get('phase')
        entry_module = entry.get('Module') or entry.get('module')
        # cast phase
        try:
            entry_phase_int = int(entry_phase)
        except:
            continue
        if phases and entry_phase_int not in phases:
            continue
        if modules and entry_module not in modules:
            continue
        # locate script path
        script_path = entry.get('Path') or entry.get('ScriptPath') or entry.get('FinalFilename') or entry.get('filename')
        if not script_path:
            continue
        filtered.append(script_path)
    return filtered


def run_scripts(scripts, dry_run):
    for script in scripts:
        print(f"\n▶ Running: {script}")
        if dry_run:
            continue
        # ensure path exists
        if not os.path.isfile(script):
            print(f"  ✗ Script not found: {script}")
            continue
        proc = subprocess.Popen(
            ['python', script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = proc.communicate()
        status = 'PASS' if proc.returncode == 0 else 'FAIL'
        # prepare log folder
        base = os.path.splitext(os.path.basename(script))[0]
        log_dir = os.path.join('outputs', 'logs', base)
        os.makedirs(log_dir, exist_ok=True)
        # write logs
        with open(os.path.join(log_dir, 'stdout.log'), 'w', encoding='utf-8') as f:
            f.write(out)
        with open(os.path.join(log_dir, 'stderr.log'), 'w', encoding='utf-8') as f:
            f.write(err)
        with open(os.path.join(log_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
            f.write(status)
        print(f"  {status}: returncode={proc.returncode}")


def main():
    args = parse_args()
    manifest = load_manifest(args.manifest)
    scripts = filter_manifest(manifest, args.phases, args.modules)
    if not scripts:
        print("No matching entries found in manifest. Nothing to run.")
        sys.exit(0)
    print(f"Found {len(scripts)} script(s) to execute.")
    run_scripts(scripts, args.dry_run)


if __name__ == '__main__':
    main()
