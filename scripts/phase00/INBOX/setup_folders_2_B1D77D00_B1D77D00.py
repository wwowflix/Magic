# -*- coding: utf-8 -*-
# setup_folders.py - Phase 1

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

print("ðŸ§± Ensuring folder structure...")
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"ðŸ“ Created: {folder}")
    else:
        print(f"âœ… Exists: {folder}")
