import os
import time

# CONFIG
TARGET_DIRS = ["outputs/logs", "outputs/tmp", "outputs/cache"]
AGE_THRESHOLD_DAYS = 1
LOG_FILE = "outputs/logs/cleanup_report.txt"

# Time threshold
now = time.time()
cutoff = now - AGE_THRESHOLD_DAYS * 86400

cleaned_files = []

for folder in TARGET_DIRS:
    if not os.path.exists(folder):
        continue
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                cleaned_files.append(path)
                os.remove(path)

# Write cleanup report
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if cleaned_files:
        f.write("🧹 Cleanup Report:\n")
        for file in cleaned_files:
            f.write(f"Deleted: {file}\n")
    else:
        f.write("✅ No outdated files found.\n")

print(f"📄 Cleanup log saved to: {LOG_FILE}")
