#!/usr/bin/env python3
"""
Phase 11 - Module A
Script: Script Health Verifier
Purpose:
- Scans all _READY.py scripts in Phase 11.
- Verifies each has a main() function and no syntax errors.
- Logs results to outputs/logs/script_health_report.txt
"""

import os
import subprocess

PHASE_PATH = r"D:\MAGIC\scripts\phase11"
LOG_FILE = r"D:\MAGIC\outputs\logs\script_health_report.txt"

def main():
    try:
        bad_scripts = []

        with open(LOG_FILE, "w", encoding="utf-8") as log:
            for root, _, files in os.walk(PHASE_PATH):
                for file in files:
                    if file.endswith("_READY.py"):
                        filepath = os.path.join(root, file)
                        # Syntax check
                        result = subprocess.run(["python", "-m", "py_compile", filepath],
                                                capture_output=True, text=True)
                        if result.returncode != 0:
                            bad_scripts.append(file)
                            log.write(f"❌ Syntax error: {file}\n")
                        else:
                            # Check for main()
                            with open(filepath, encoding="utf-8") as f:
                                content = f.read()
                                if "def main" not in content:
                                    bad_scripts.append(file)
                                    log.write(f"⚠️ Missing main(): {file}\n")

            if not bad_scripts:
                log.write("✅ All scripts passed health check.\n")

        print("PASS")
    except Exception as e:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"❌ Error occurred: {str(e)}\n")
        print("FAIL")

if __name__ == "__main__":
    main()
