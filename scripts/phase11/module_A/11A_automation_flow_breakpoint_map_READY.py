#!/usr/bin/env python3
# MAGIC_DYNAMIC_ROOTS_V3
import os
from pathlib import Path

# --- Root Discovery (Drive-Agnostic) ---
_ROOT = Path(__file__).resolve()
_tmp = _ROOT
for _ in range(6):
    if (_tmp / ".git").exists() or (_tmp / "outputs").exists():
        _ROOT = _tmp
        break
    _tmp = _tmp.parent
else:
    _ROOT = Path(__file__).resolve().parents[4]

LOG_DIR = _ROOT / "outputs" / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

PHASE_PATH = _ROOT / "scripts" / "phase11"
LOG_FILE = LOG_DIR / "automation_breakpoints_report.txt"


def main():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)

        modules = [
            d for d in PHASE_PATH.iterdir()
            if d.is_dir()
        ]

        with open(LOG_FILE, "w", encoding="utf-8") as log:
            for module in sorted(modules):
                ready_files = list(module.glob("*_READY.py"))

                if len(ready_files) == 0:
                    log.write(f"[BREAKPOINT] Module '{module.name}' has **NO** scripts.\n")
                elif len(ready_files) < 3:
                    log.write(f"[WEAK] Module '{module.name}' has only {len(ready_files)} scripts.\n")
                else:
                    log.write(f"[OK] Module '{module.name}' is complete ({len(ready_files)} scripts).\n")

        print("OK")
    except Exception as e:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"[ERROR] {str(e)}\n")
        print("FAIL")


if __name__ == "__main__":
    main()
