import os
import subprocess
import json
from datetime import datetime
from collections import defaultdict

# Load manifest with utf-8-sig encoding
with open("phase_manifest.json", "r", encoding="utf-8-sig") as f:
    manifest = json.load(f)

LOGS_BASE = os.path.join("outputs", "logs")
SUMMARY_BASE = os.path.join("outputs", "summaries")
os.makedirs(LOGS_BASE, exist_ok=True)
os.makedirs(SUMMARY_BASE, exist_ok=True)

MAX_RETRIES = 2


def run_script(phase, module, script_path):
    log_folder = os.path.join(LOGS_BASE, f"phase{phase}_module_{module}")
    os.makedirs(log_folder, exist_ok=True)

    script_name = os.path.basename(script_path)
    log_file = os.path.join(log_folder, script_name.replace(".py", ".log"))

    for attempt in range(1, MAX_RETRIES + 1):
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"=== Run Started: {datetime.now()} (Attempt {attempt}) ===\n")
            log.write(f"Running script: {script_path}\n\n")
            try:
                result = subprocess.run(
                    ["python", script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300,
                )
                log.write("--- STDOUT ---\n")
                log.write(result.stdout + "\n")
                log.write("--- STDERR ---\n")
                log.write(result.stderr + "\n")
                log.write(f"Exit Code: {result.returncode}\n")
                log.write(f"=== Run Ended: {datetime.now()} ===\n\n")

                if result.returncode == 0:
                    return 0
                else:
                    log.write(f"[WARNING] Script failed on attempt {attempt}.\n\n")
            except Exception as e:
                log.write(f"[ERROR] Exception while running script: {e}\n\n")

        if attempt < MAX_RETRIES:
            print(f"[WARNING] {script_name} failed on attempt {attempt}. Retrying...")
        else:
            print(f"[FAIL] {script_name} failed after {MAX_RETRIES} attempts.")
    return 1  # Failed after max retries


def main():
    print(
        f"\n▶ Starting Self-Healing Runner v4.6 with per-module summaries on {len(manifest)} scripts...\n"
    )

    total = 0
    passed = 0
    failed = 0

    results = defaultdict(list)

    for script_path in manifest:
        parts = os.path.normpath(script_path).split(os.sep)
        if len(parts) < 3:
            print(f"[WARNING] Unexpected script path format: {script_path}")
            failed += 1
            continue

        phase = parts[-3].replace("phase", "")
        module = parts[-2].replace("module_", "")

        if not os.path.exists(script_path):
            print(f"[WARNING] Missing script: {script_path}")
            failed += 1
            results[(phase, module)].append((os.path.basename(script_path), "MISSING"))
            continue

        print(f"▶ Running: {os.path.basename(script_path)}")
        code = run_script(phase, module, script_path)

        total += 1
        status = "PASS" if code == 0 else "FAIL"
        if code == 0:
            passed += 1
        else:
            failed += 1

        results[(phase, module)].append((os.path.basename(script_path), status))

    for (phase, module), scripts in results.items():
        summary_path = os.path.join(
            SUMMARY_BASE, f"phase{phase}_module_{module}_summary.tsv"
        )
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("Script\tStatus\n")
            for script_name, status in scripts:
                f.write(f"{script_name}\t{status}\n")

    print("\n=== SUMMARY ===")
    print(f"Total scripts: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Per-module summaries saved in: {SUMMARY_BASE}\n")


if __name__ == "__main__":
    main()
