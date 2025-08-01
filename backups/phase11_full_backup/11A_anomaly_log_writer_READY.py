import os
import time
from datetime import datetime

# Define the log directory and anomaly log output path
LOG_DIR = "logs"
ANOMALY_LOG = os.path.join(LOG_DIR, "anomalies_detected.log")

# Keywords that indicate anomalies
ANOMALY_KEYWORDS = ["ERROR", "WARNING", "FAILURE", "CRITICAL", "UNAUTHORIZED", "EXCEPTION"]

def scan_logs_for_anomalies():
    print("🔍 Scanning logs for anomalies...")
    found = False
    summary = []

    for root, _, files in os.walk(LOG_DIR):
        for file in files:
            if file.endswith(".log") and "anomalies_detected" not in file:
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_number, line in enumerate(f, 1):
                        for keyword in ANOMALY_KEYWORDS:
                            if keyword in line:
                                found = True
                                summary.append(f"{file} [Line {line_number}]: {line.strip()}")

    if found:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ANOMALY_LOG, "a", encoding="utf-8") as out:
            out.write(f"\n=== Anomaly Report @ {timestamp} ===\n")
            for entry in summary:
                out.write(entry + "\n")
        print(f"🚨 {len(summary)} anomalies found. Written to anomalies_detected.log.")
    else:
        print("✅ No anomalies found.")

if __name__ == "__main__":
    scan_logs_for_anomalies()
