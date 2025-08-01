#!/usr/bin/env python3
"""
MAGIC Project - Phase 11 Awareness Layer
----------------------------------------
Script: 11A_anomaly_log_writer_READY.py
Role:
    - Scan MAGIC logs for anomalies (errors, repeated patterns, missing file warnings)
    - Write all detected anomalies to anomaly_flags.log
"""

import os
import time
from collections import Counter

LOG_DIR = r"D:\MAGIC\logs"
MASTER_LOG = os.path.join(LOG_DIR, "magic_master_log.txt")
ANOMALY_LOG = os.path.join(LOG_DIR, "anomaly_flags.log")

# Ensure log folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def detect_anomalies(lines):
    anomalies = []

    # Count occurrences of log entries
    counter = Counter(lines)

    # Detect repetitive spam logs
    for entry, count in counter.items():
        if count > 5:
            anomalies.append(f"[REPEAT-SPAM] '{entry.strip()}' appeared {count} times.")

    # Detect error/warning patterns
    for line in lines:
        if "error" in line.lower() or "❌" in line or "failed" in line.lower():
            anomalies.append(f"[ERROR-DETECTED] {line.strip()}")

    return anomalies

def write_anomalies(anomalies):
    if anomalies:
        with open(ANOMALY_LOG, "a", encoding="utf-8") as f:
            for anomaly in anomalies:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {anomaly}\n")

def main():
    print("🔍 Anomaly Log Writer Agent started...")

    last_size = 0
    while True:
        if os.path.exists(MASTER_LOG):
            with open(MASTER_LOG, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Only analyze new lines since last read
            new_lines = lines[last_size:]
            last_size = len(lines)

            anomalies = detect_anomalies(new_lines)
            write_anomalies(anomalies)

        time.sleep(3)

if __name__ == "__main__":
    main()
