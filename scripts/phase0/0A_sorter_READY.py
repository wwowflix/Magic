"""
Phase 0A – Sorter Script
This script moves files from the inbox to the correct phase/module folder
based on naming convention like `02A_google_trends_scraper_READY.py`.
"""

import os
import re
import shutil
from datetime import datetime

# Root paths
ROOT = r"D:\MAGIC"
INBOX = os.path.join(ROOT, "inbox")
SCRIPTS = os.path.join(ROOT, "scripts")
LOGS = os.path.join(ROOT, "logs", "phase0")

os.makedirs(LOGS, exist_ok=True)
log_file = os.path.join(LOGS, "0A_sorter.log")

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

# Regex: e.g., 02A_google_trends_scraper_READY.py
pattern = re.compile(r"^(?P<phase>\d{2})(?P<module>[A-Z])_.*_READY\.py$")

def main():
    if not os.path.exists(INBOX):
        log("Inbox missing, nothing to process.")
        return

    for fname in os.listdir(INBOX):
        fpath = os.path.join(INBOX, fname)
        if not os.path.isfile(fpath):
            continue

        m = pattern.match(fname)
        if not m:
            log(f"Skipped: {fname} (invalid format)")
            continue

        phase = f"phase{int(m.group('phase'))}"
        module = f"module_{m.group('module')}"
        dest_dir = os.path.join(SCRIPTS, phase, module)
        os.makedirs(dest_dir, exist_ok=True)

        dest = os.path.join(dest_dir, fname)
        shutil.move(fpath, dest)
        log(f"Moved {fname} → {dest}")

if __name__ == "__main__":
    main()
