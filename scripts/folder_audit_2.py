# -*- coding: utf-8 -*-
# folder_audit.py
# Phase 1 – Folder Health Checker

import os

REQUIRED_FOLDERS = [
    "inputs",
    "outputs",
    "logs",
    "configs",
    "scripts",
    "temp",
    "dashboards",
    "tests",
]

def check_folders(base_path="."):
    print("?? Scanning folder health...\n")
    missing = []

    for folder in REQUIRED_FOLDERS:
        full_path = os.path.join(base_path, folder)
        if not os.path.exists(full_path):
            print(f"? Missing: {full_path}")
            missing.append(full_path)
        else:
            print(f"? Found:   {full_path}")

    if not missing:
        print("\n?? All required folders are present!")
    else:
        print(f"\n?? {len(missing)} folders missing. You can auto-create them using `setup_folders.py`")

if __name__ == "__main__":
    check_folders()

