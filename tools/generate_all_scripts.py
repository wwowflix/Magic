#!/usr/bin/env python
"""
generate_all_scripts.py

Safely generates missing *_READY.py stub scripts for MAGIC phases.

Rules:
- Scan scripts root for folders named 'phase*'
- For each subfolder (module) under a phase:
  - If there is NO file matching '*_READY.py', create one stub:
    <phase_name>_<module_name}_auto_READY.py
- Do NOT overwrite any existing files.
- Write a TSV manifest summarizing actions.

Usage:
    python tools/generate_all_scripts.py --root E:\\MAGIC\\scripts
    python tools/generate_all_scripts.py --root E:\\MAGIC\\scripts --dry-run
"""

from __future__ import annotations
import argparse
from pathlib import Path
import sys
from datetime import datetime

STUB_TEMPLATE = '''"""MAGIC auto-generated stub.

Phase: {phase_name}
Module: {module_name}
Relative Path: {rel_path}

This file was created automatically by tools/generate_all_scripts.py
to ensure that every phase/module has at least one *_READY.py script.

You can safely replace the contents with real logic later.
"""

def run():
    """
    Entry point for this MAGIC script.
    Currently a placeholder; implement real logic in later stages.
    """
    return {{
        "status": "OK",
        "phase": "{phase_name}",
        "module": "{module_name}",
        "auto_generated": True,
    }}
'''

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help="Root scripts folder, e.g. E:\\MAGIC\\scripts",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without writing files",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"[ERROR] Scripts root does not exist: {root}", file=sys.stderr)
        return 1

    repo_root = root.parents[0]  # assumes <repo>/scripts
    outputs_dir = repo_root / "outputs" / "reports"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = outputs_dir / "generation_manifest.tsv"

    lines = []
    header = "phase\tmodule\tstub_path\taction\tdry_run\ttimestamp"
    lines.append(header)

    created_count = 0
    skipped_count = 0

    phase_dirs = sorted([p for p in root.iterdir() if p.is_dir() and p.name.startswith("phase")])

    ts = datetime.utcnow().isoformat() + "Z"

    for phase_dir in phase_dirs:
        phase_name = phase_dir.name  # e.g. phase11
        module_dirs = sorted([m for m in phase_dir.iterdir() if m.is_dir()])

        if not module_dirs:
            # phases without modules are allowed but logged
            rel = phase_dir.relative_to(repo_root)
            line = f"{phase_name}\t-\t{rel}\tNO_MODULES\tdry_run={args.dry_run}\t{ts}"
            lines.append(line)
            continue

        for module_dir in module_dirs:
            module_name = module_dir.name  # e.g. A, B, other
            existing_ready = list(module_dir.glob("*_READY.py"))

            if existing_ready:
                # Already has at least one READY script
                rel = existing_ready[0].relative_to(repo_root)
                lines.append(
                    f"{phase_name}\t{module_name}\t{rel}\tSKIP_ALREADY_HAS_READY\tdry_run={args.dry_run}\t{ts}"
                )
                skipped_count += 1
                continue

            # Need to create a stub
            stub_name = f"{phase_name}_{module_name}_auto_READY.py"
            stub_path = module_dir / stub_name
            rel = stub_path.relative_to(repo_root)

            if args.dry_run:
                action = "WOULD_CREATE"
            else:
                contents = STUB_TEMPLATE.format(
                    phase_name=phase_name,
                    module_name=module_name,
                    rel_path=rel.as_posix(),
                )
                stub_path.write_text(contents, encoding="utf-8")
                action = "CREATED"

            lines.append(
                f"{phase_name}\t{module_name}\t{rel}\t{action}\tdry_run={args.dry_run}\t{ts}"
            )
            if not args.dry_run:
                created_count += 1

    # Write manifest
    manifest_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Scan complete for root: {root}")
    print(f"    READY stubs created: {created_count}")
    print(f"    Modules skipped (already had READY): {skipped_count}")
    print(f"    Manifest: {manifest_path}")

    if args.dry_run:
        print("[INFO] Dry-run mode: no files were actually written.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
