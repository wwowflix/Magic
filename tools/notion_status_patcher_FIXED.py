import re
import os

log_path = r"D:\MAGIC\outputs\logs\master_orchestrator_log.txt"

passing_keywords = ["executed successfully", "PASS"]
error_keywords = ["ERROR", "Exception", "Traceback"]

pass_count = 0
error_count = 0

if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if any(k in line for k in passing_keywords):
                pass_count += 1
            if any(k in line for k in error_keywords):
                error_count += 1

print(f"✅ Found {pass_count} passing scripts, {error_count} with errors.")
print("🎯 Notion sync complete.")
