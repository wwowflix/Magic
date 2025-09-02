# tools/generate_patch_csv.py

import csv
import os
from pathlib import Path

MAGIC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_FOLDER = MAGIC_ROOT / "scripts"
PATCH_CSV = MAGIC_ROOT / "magic_patch.csv"

def extract_metadata(file_path):
    filename = file_path.name
    parts = filename.split("_")
    phase_module = parts[0]
    phase = int(phase_module[0:2])
    module = phase_module[2]
    status = "READY"
    folder_location = str(file_path.parent.relative_to(MAGIC_ROOT)).replace("\\", "/")
    is_placeholder = "False"
    is_implemented = "True"
    return {
        "Filename": filename,
        "Phase": phase,
        "Module": module,
        "Status": status,
        "Folder Location": folder_location,
        "Is Placeholder": is_placeholder,
        "Is Implemented": is_implemented,
    }

def collect_files():
    py_files = SCRIPTS_FOLDER.rglob("*_READY.py")
    return [extract_metadata(f) for f in py_files]

def write_csv(data):
    with open(PATCH_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "Phase", "Module", "Status", "Folder Location", "Is Placeholder", "Is Implemented"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    data = collect_files()
    write_csv(data)
    print(f"✅ Patch CSV generated: {PATCH_CSV}")

if __name__ == "__main__":
    main()
