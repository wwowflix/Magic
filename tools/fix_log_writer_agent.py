#!/usr/bin/env python3
r"""
MAGIC Project â€“ Log Writer Auto-Fix Script
Author: ChatGPT Assistant
Purpose:
    - Check if target script exists
    - Create placeholder if missing
    - Write a timestamped log entry
    - Ensure D:\MAGIC\logs exists and log file is updated
r"""

import os
import sys
from datetime import datetime

# ------------------------------
# CONFIGURATION
# ------------------------------
PROJECT_ROOT = r"D:\MAGIC"
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
TARGET_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "phase11", "module_l", "11L_rate_limit_guard_READY.py")
MASTER_LOG = os.path.join(LOGS_DIR, "magic_master_log.txt")

# ------------------------------
# 1ï¸âƒ£ Ensure logs directory exists
# ------------------------------
os.makedirs(LOGS_DIR, exist_ok=True)

# ------------------------------
# 2ï¸âƒ£ Ensure target script exists
# ------------------------------
if not os.path.exists(TARGET_SCRIPT):
    os.makedirs(os.path.dirname(TARGET_SCRIPT), exist_ok=True)
    with open(TARGET_SCRIPT, "w", encoding="utf-8") as f:
        f.write("# Auto-created placeholder script\n")
        f.write("print('11L_rate_limit_guard_READY is running...')\n")
    print(f"ðŸ†• Created missing script: {TARGET_SCRIPT}")
else:
    print(f"âœ… Script found: {TARGET_SCRIPT}")

# ------------------------------
# 3ï¸âƒ£ Write to log
# ------------------------------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] âœ… Checked & ensured script exists: {TARGET_SCRIPT}\n"

with open(MASTER_LOG, "a", encoding="utf-8") as log:
    log.write(log_entry)

print(f"ðŸ“ Log updated: {MASTER_LOG}")
print("âœ… Fix Log Writer Agent process completed.")

