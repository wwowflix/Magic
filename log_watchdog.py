import os
import time

LOGS_DIR = os.path.join("outputs", "logs")
ALERTS_DIR = os.path.join("outputs", "alerts")
ALERT_FILE = os.path.join(ALERTS_DIR, "watchdog_report.log")
ERROR_KEYWORDS = ["traceback", "error", "exception"]
CHECK_INTERVAL = 30  # seconds


def scan_log_for_errors(log_path):
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return any(keyword in content for keyword in ERROR_KEYWORDS)
    except Exception:
        return False


def main():
    os.makedirs(ALERTS_DIR, exist_ok=True)
    seen_files = {}

    print(f"🛡️ Starting Log Watchdog, monitoring folder: {LOGS_DIR}")
    while True:
        for root, _, files in os.walk(LOGS_DIR):
            for file in files:
                if not file.endswith(".log"):
                    continue
                file_path = os.path.join(root, file)
                last_modified = os.path.getmtime(file_path)

                # Check if file is new or updated
                if file_path not in seen_files or seen_files[file_path] < last_modified:
                    seen_files[file_path] = last_modified

                    if scan_log_for_errors(file_path):
                        alert_msg = f"[ALERT] Error found in log: {file_path}\n"
                        print(alert_msg.strip())

                        with open(ALERT_FILE, "a", encoding="utf-8") as alert_log:
                            alert_log.write(alert_msg)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
