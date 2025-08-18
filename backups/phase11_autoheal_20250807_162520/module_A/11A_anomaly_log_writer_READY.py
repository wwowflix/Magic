import os
from datetime import datetime

ANOMALY_LOG_PATH = r"D:\MAGIC\logs\anomaly_flags.log"
SCRIPTS_FOLDER = r"D:\MAGIC\scripts\phase11"


def check_for_missing_scripts():
    missing = []
    # Example: Check for expected placeholder scripts existence
    expected_scripts = [
        "11A_some_script_READY.py",
        "11B_auto_recover_agent_READY.py",
        # Add all critical scripts expected in Phase 11
    ]
    for script in expected_scripts:
        script_path = os.path.join(
            SCRIPTS_FOLDER, "module_A", script
        )  # adjust module path as needed
        if not os.path.exists(script_path):
            missing.append(script)
    return missing


def log_anomalies(anomalies):
    if not anomalies:
        return
    with open(ANOMALY_LOG_PATH, "a", encoding="utf-8") as f:
        for anomaly in anomalies:
            f.write(f"{datetime.now()} | MISSING SCRIPT | {anomaly}\n")
    print(f"Anomalies logged: {len(anomalies)}")


def main():
    anomalies = check_for_missing_scripts()
    log_anomalies(anomalies)


if __name__ == "__main__":
    main()
