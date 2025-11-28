from __future__ import annotations
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

SHIM = '''from __future__ import annotations

"""
MAGIC Week 0 Shim for scripts.{module}
Auto-generated to make imports safe.
"""

class Placeholder:
    ...

def main(*args, **kwargs):
    return 0

__all__ = ["Placeholder", "main"]
'''

def main():
    list_file = pathlib.Path(sys.argv[1]).resolve()
    modules = [line.strip() for line in list_file.read_text().splitlines()
               if line.strip().startswith("scripts.")]

    print(f"Found {len(modules)} modules to shim.\n")

    for full in modules:
        base = full.split(".", 1)[1]
        target = SCRIPTS_DIR / f"{base}.py"
        backup = SCRIPTS_DIR / f"{base}.py.magic_bak_week0"

        if not target.exists():
            print(f"[SKIP - NOT FOUND] {full}")
            continue

        if not backup.exists():
            print(f"[BACKUP] {full} → {backup.name}")
            target.rename(backup)
        else:
            print(f"[OK] Backup already exists")

        print(f"[WRITE] Generating shim for {full}")
        target.write_text(SHIM.format(module=base), encoding="utf-8")

    print("\nALL SHIMS GENERATED.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
