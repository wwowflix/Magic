import os
import time
import random

# CONFIG
LOG_FILE = "outputs/logs/bottleneck_profile_log.txt"
PHASES = 3
TASKS_PER_PHASE = 5


def simulate_task(phase, task_id):
    delay = random.uniform(0.1, 0.7)
    time.sleep(delay)
    return f"Phase {phase} - Task {task_id} â†’ Took {delay:.2f}s"


# Ensure log folder
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("ðŸ¢ Bottleneck Profiling Started\n")
    for phase in range(1, PHASES + 1):
        for task in range(1, TASKS_PER_PHASE + 1):
            result = simulate_task(phase, task)
            print(result)
            f.write(result + "\n")

    f.write("âœ… Bottleneck profiling complete.\n")

print(f"ðŸ“„ Log saved to: {LOG_FILE}")
