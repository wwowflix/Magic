# -*- coding: utf-8 -*-
# setup_folders.py – Phase 1

import os

REQUIRED_FOLDERS = [
    "inputs",
    "outputs",
    "logs",
    "configs",
    "scripts",
    "tests",
    "temp",
    "dashboards",
]

print("🧱 Ensuring folder structure...")
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created: {folder}")
    else:
        print(f"✅ Exists: {folder}")
