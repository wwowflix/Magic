import os
import time
import glob

LOGS_DIR = "outputs/logs"
ALERTS_DIR = "outputs/alerts"
CHECK_INTERVAL = 60  # seconds

os.makedirs(ALERTS_DIR, exist_ok=True)


def check_logs():
    log_files = glob.glob(os.path.join(LOGS_DIR, "**", "*.log"), recursive=True)
    alerts = []
    for log_file in log_files:
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if any(err in content for err in ["traceback", "error", "exception"]):
                    alerts.append(f"[ALERT] Error found in log: {log_file}")
        except Exception as e:
            alerts.append(f"[ERROR] Could not read {log_file}: {e}")

    if alerts:
        alert_path = os.path.join(ALERTS_DIR, "watchdog_report.log")
        with open(alert_path, "a", encoding="utf-8") as alert_file:
            for alert in alerts:
                print(alert)
                alert_file.write(alert + "\n")


def main():
    print("🛡️  Starting Log Watchdog. Press Ctrl+C to stop.")
    try:
        while True:
            check_logs()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Log Watchdog stopped by user gracefully.")


if __name__ == "__main__":
    main()
