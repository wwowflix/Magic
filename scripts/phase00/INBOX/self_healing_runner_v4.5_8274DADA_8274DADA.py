import os
import subprocess
import json
from datetime import datetime

# Load manifest with utf-8-sig encoding
with open("phase_manifest.json", "r", encoding="utf-8-sig") as f:
    manifest = json.load(f)

LOGS_BASE = os.path.join("outputs", "logs")
os.makedirs(LOGS_BASE, exist_ok=True)

MAX_RETRIES = 2


def run_script(phase, module, script_path):
    log_folder = os.path.join(LOGS_BASE, f"phase{phase}_module_{module}")
    os.makedirs(log_folder, exist_ok=True)

    script_name = os.path.basename(script_path)
    log_file = os.path.join(log_folder, script_name.replace(".py", ".log"))

    for attempt in range(1, MAX_RETRIES + 1):
        with open(log_file, "a", encoding="utf-8") as log:  # Append logs for retries
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
                    log.write(f"⚠️ Script failed on attempt {attempt}.\n\n")
            except Exception as e:
                log.write(f"[ERROR] Exception while running script: {e}\n\n")

        if attempt < MAX_RETRIES:
            print(
                f"⚠️ {os.path.basename(script_path)} failed on attempt {attempt}. Retrying..."
            )
        else:
            print(
                f"❌ {os.path.basename(script_path)} failed after {MAX_RETRIES} attempts."
            )

    return 1  # Failure after max retries


def main():
    print(
        f"\n▶ Starting Self-Healing Runner v4.5 with retry logic on {len(manifest)} scripts...\n"
    )

    total = 0
    passed = 0
    failed = 0

    for script_path in manifest:
        parts = os.path.normpath(script_path).split(os.sep)
        if len(parts) < 3:
            print(f"⚠️ Unexpected script path format: {script_path}")
            failed += 1
            continue

        phase = parts[-3].replace("phase", "")
        module = parts[-2].replace("module_", "")

        if not os.path.exists(script_path):
            print(f"⚠️ Missing script: {script_path}")
            failed += 1
            continue

        print(f"▶ Running: {os.path.basename(script_path)}")
        code = run_script(phase, module, script_path)

        total += 1
        if code == 0:
            print(f"✅ PASS: {os.path.basename(script_path)}")
            passed += 1
        else:
            failed += 1

    print("\n=== SUMMARY ===")
    print(f"Total scripts: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Logs saved to: {LOGS_BASE}\n")


if __name__ == "__main__":
    main()
