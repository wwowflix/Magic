#!/usr/bin/env python3
"""
MAGIC PROJECT - PHASE 11
Awareness Agent: Log Writer

🔹 Purpose:
    - Run specified script(s) and log results with timestamps.
    - Store logs in D:\MAGIC\logs\magic_master_log.txt
    - Helps track script execution and errors automatically.

Usage:
    python agents/awareness/log_writer_agent.py <script_or_folder_path>

Example:
    python agents/awareness/log_writer_agent.py scripts/phase11/module_l/11L_rate_limit_guard_READY.py
    python agents/awareness/log_writer_agent.py scripts/phase11/module_l
"""

import os
import sys
import subprocess
from datetime import datetime

# --- CONFIG ---
PROJECT_ROOT = r"D:\MAGIC"
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "magic_master_log.txt")


def ensure_log_dir():
    """Ensure logs folder exists"""
    os.makedirs(LOG_DIR, exist_ok=True)


def write_log(message):
    """Write a timestamped log entry"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"📝 LOGGED: {message}")


def run_and_log(script_path):
    """Execute a Python script and log its output and errors"""
    abs_path = os.path.abspath(script_path)
    if not os.path.exists(abs_path):
        write_log(f"❌ Target script not found: {abs_path}")
        return

    write_log(f"🚀 Starting script: {abs_path}")
    try:
        result = subprocess.run(
            ["python", abs_path],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout:
            write_log(f"✅ OUTPUT:\n{result.stdout.strip()}")
        if result.stderr:
            write_log(f"⚠️ ERRORS:\n{result.stderr.strip()}")
    except Exception as e:
        write_log(f"❌ Failed to run script {abs_path}: {str(e)}")
    finally:
        write_log(f"🏁 Finished script: {abs_path}\n")


def main():
    ensure_log_dir()

    if len(sys.argv) < 2:
        print("⚠️ Usage: python log_writer_agent.py <script_or_folder_path>")
        sys.exit(1)

    target_path = os.path.normpath(sys.argv[1])

    # If folder given → process all READY scripts
    if os.path.isdir(target_path):
        for file in sorted(os.listdir(target_path)):
            if file.endswith("_READY.py"):
                run_and_log(os.path.join(target_path, file))
    else:
        run_and_log(target_path)


if __name__ == "__main__":
    main()
