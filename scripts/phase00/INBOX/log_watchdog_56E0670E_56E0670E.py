from __future__ import annotations

import os
import time
from typing import Dict


LOGS_DIR = os.path.join("outputs", "logs")
ALERTS_DIR = os.path.join("outputs", "alerts")
ALERT_FILE = os.path.join(ALERTS_DIR, "watchdog_report.log")
ERROR_KEYWORDS = ["traceback", "error", "exception"]
CHECK_INTERVAL = 30  # seconds


def scan_log_for_errors(log_path: str) -> bool:
    """
    Return True if the log file at `log_path` appears to contain
    any error-like keywords, False otherwise.
    """
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return any(keyword in content for keyword in ERROR_KEYWORDS)
    except Exception:
        # On any read error, just treat as "no errors found" for now.
        return False


def main() -> None:
    """
    MAGIC log watchdog.

    Normal mode:
        - Runs forever, sleeping CHECK_INTERVAL between scans.
        - Scans outputs/logs for *.log files.
        - When new/updated logs contain error keywords, appends an alert
          line to outputs/alerts/watchdog_report.log.

    Pytest mode:
        - Detected via the PYTEST_CURRENT_TEST environment variable.
        - Uses a tiny interval and runs only a single loop iteration,
          then returns so the smoke test does not hang.
    """
    os.makedirs(ALERTS_DIR, exist_ok=True)
    seen_files: Dict[str, float] = {}

    # Detect if we are running under pytest
    under_pytest = "PYTEST_CURRENT_TEST" in os.environ

    interval = CHECK_INTERVAL
    max_loops: int | None = None

    if under_pytest:
        # Fast, single-iteration mode for tests
        interval = 0.01
        max_loops = 1

    print(f"[MAGIC] Starting Log Watchdog, monitoring folder: {LOGS_DIR}")
    loops = 0

    while True:
        for root, _, files in os.walk(LOGS_DIR):
            for file in files:
                if not file.endswith(".log"):
                    continue

                file_path = os.path.join(root, file)
                try:
                    last_modified = os.path.getmtime(file_path)
                except OSError:
                    # If the file disappears mid-scan, just skip it
                    continue

                # Check if file is new or updated
                if file_path not in seen_files or seen_files[file_path] < last_modified:
                    seen_files[file_path] = last_modified

                    if scan_log_for_errors(file_path):
                        alert_msg = f"[ALERT] Error found in log: {file_path}\n"
                        print(alert_msg.strip())

                        try:
                            with open(ALERT_FILE, "a", encoding="utf-8") as alert_log:
                                alert_log.write(alert_msg)
                        except Exception:
                            # Don't crash the watchdog if the alert file fails
                            print("[MAGIC] Failed to write to alert log file:", ALERT_FILE)

        loops += 1
        if max_loops is not None and loops >= max_loops:
            # In pytest mode we exit quickly so smoke tests don't hang
            return

        time.sleep(interval)


if __name__ == "__main__":
    main()
