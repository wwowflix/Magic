#!/usr/bin/env python3
"""
Phase 11 - Module A
Script: Automation Flow Breakpoint Map
Purpose:
- Scans Phase 11 modules.
- Detects folders with zero scripts or incomplete sets.
- Logs potential "breakpoints" in the automation flow.
"""

import os

PHASE_PATH = r"D:\MAGIC\scripts\phase11"
LOG_FILE = r"D:\MAGIC\outputs\logs\automation_breakpoints_report.txt"


def main():
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            modules = sorted(
                [
                    d
                    for d in os.listdir(PHASE_PATH)
                    if os.path.isdir(os.path.join(PHASE_PATH, d))
                ]
            )
            for module in modules:
                files = [
                    f
                    for f in os.listdir(os.path.join(PHASE_PATH, module))
                    if f.endswith("_READY.py")
                ]
                if len(files) == 0:
                    log.write(f"❌ Breakpoint: {module} has NO scripts.\n")
                elif len(files) < 3:
                    log.write(
                        f"⚠️ Potential issue: {module} has only {len(files)} scripts.\n"
                    )
                else:
                    log.write(
                        f"✅ Module {module} looks okay ({len(files)} scripts).\n"
                    )

        print("PASS")
    except Exception as e:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"❌ Error occurred: {str(e)}\n")
        print("FAIL")


if __name__ == "__main__":
    main()
