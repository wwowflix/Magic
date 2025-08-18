#!/usr/bin/env python3
"""
Phase 11 - Module A
Script: Missing Module Detector
Purpose:
- Scans the Phase 11 folder structure.
- Compares against your CSV master file.
- Logs missing scripts to outputs/logs/missing_scripts_report.txt
"""

import csv
import os

PHASE_PATH = r"D:\MAGIC\scripts\phase11"
CSV_FILE = r"D:\MAGIC\Fulfinal_File_CLEANED.csv"
LOG_FILE = r"D:\MAGIC\outputs\logs\missing_scripts_report.txt"


def main():
    try:
        expected_files = set()
        missing_files = []

        # Read expected filenames for phase 11
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("PhaseNumber") == "11":
                    expected_files.add(row["FinalFilename"].strip())

        # Check filesystem
        found_files = set()
        for root, _, files in os.walk(PHASE_PATH):
            for f in files:
                if f.endswith("_READY.py"):
                    found_files.add(f)

        for file in expected_files:
            if file not in found_files:
                missing_files.append(file)

        with open(LOG_FILE, "w", encoding="utf-8") as log:
            if missing_files:
                log.write("MISSING FILES DETECTED:\n")
                for mf in missing_files:
                    log.write(f"- {mf}\n")
            else:
                log.write("✅ No missing files. All expected scripts are present.\n")

        print("PASS")
    except Exception as e:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"❌ Error occurred: {str(e)}\n")
        print("FAIL")


if __name__ == "__main__":
    main()
