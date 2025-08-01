import os
import random
import time

# CONFIG
LOG_FILE = "outputs/logs/budget_burn_log.txt"
CATEGORIES = {
    'API Calls': 1200,
    'Compute Time': 85,  # % CPU
    'Disk I/O': 300,     # MB/s
    'Memory Use': 75     # % RAM
}

# Simulate monitoring
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("💸 Budget Burn Monitor Started\n")
    for name, threshold in CATEGORIES.items():
        usage = round(random.uniform(threshold - 20, threshold + 20), 2)
        status = "⚠️ Exceeded" if usage > threshold else "✅ OK"
        log_line = f"{name}: {usage} → {status} (Limit: {threshold})"
        print(log_line)
        f.write(log_line + "\n")
    f.write("✅ Monitoring complete.\n")

print(f"📄 Budget report saved to: {LOG_FILE}")
