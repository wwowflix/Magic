import os
import random
import magic_time as time

# CONFIG
FAILPOINTS = [
    "network_timeout",
    "file_corruption",
    "unexpected_exit",
    "api_rate_limit_exceeded",
    "disk_full",
]
LOG_FILE = "outputs/logs/failpoint_simulation_log.txt"

# Simulate failures
os.makedirs("outputs/logs", exist_ok=True)

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("🧪 Failpoint Simulation Started\n")
    for i in range(5):
        fail = random.choice(FAILPOINTS)
        delay = round(random.uniform(0.1, 0.5), 2)
        f.write(f"Injecting failpoint: {fail} (delay {delay}s)\n")
        print(f"⚠️  {fail} simulated")
        time.sleep(delay)

    f.write("✅ Simulation complete\n")

print(f"📄 Log saved to: {LOG_FILE}")
