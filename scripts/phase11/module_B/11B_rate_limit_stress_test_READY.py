import os
import time
import random
from datetime import datetime

# CONFIG
TOTAL_REQUESTS = 50
MAX_PER_SECOND = 5
LOG_FILE = "outputs/logs/rate_limit_stress_test_log.txt"

# Function to simulate an API call
def simulate_api_call(index):
    start = datetime.now()
    time.sleep(random.uniform(0.05, 0.2))  # Simulate response time
    duration = (datetime.now() - start).total_seconds()
    return f"Request {index}: Took {duration:.3f}s"

# Rate limiting logic
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("🚦 Rate Limit Stress Test Log\n")
    for i in range(1, TOTAL_REQUESTS + 1):
        if i % MAX_PER_SECOND == 0:
            time.sleep(1)  # Pause to respect limit
        log_line = simulate_api_call(i)
        print(log_line)
        f.write(log_line + "\n")

print(f"✅ Stress test complete. See: {LOG_FILE}")
