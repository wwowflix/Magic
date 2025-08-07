import os
import time
import psutil
import json
from datetime import datetime

# === Configuration ===
SCRIPT_DIR = "scripts"
OUTPUT_DIR = "outputs/logs/agent_metrics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan_scripts(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("_READY.py") and not file.startswith("11F_agent_performance_log"):
                yield os.path.join(root, file)

def measure_script(script_path):
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = process.memory_info().rss

    exit_code = os.system(f"python {script_path}")

    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = process.memory_info().rss
    end_time = time.time()

    return {
        "script": script_path,
        "exit_code": exit_code,
        "cpu_delta_percent": cpu_after - cpu_before,
        "mem_usage_bytes": mem_after - mem_before,
        "execution_time_sec": round(end_time - start_time, 2)
    }

def save_results(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"agent_metrics_{timestamp}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"[PASS] Metrics saved to: {output_path}")

def main():
    all_results = []
    for script_path in scan_scripts("scripts/phase11/module_f"):
        print(f"▶ Measuring: {script_path}")
        result = measure_script(script_path)
        all_results.append(result)

    save_results(all_results)
    print("[PASS] Agent performance logging complete.")

if __name__ == "__main__":
    main()

