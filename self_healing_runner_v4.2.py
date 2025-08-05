import json
import subprocess
import os
from datetime import datetime

# Load manifest
with open("phase_manifest.json", encoding="utf-8-sig") as f:
    manifest = json.load(f)

log_dir = "outputs/logs"
summary_file = "outputs/summaries/self_healing_summary.tsv"

os.makedirs(log_dir, exist_ok=True)
os.makedirs(os.path.dirname(summary_file), exist_ok=True)

summary_lines = ["Script\tStatus\tErrorType"]

for script_path in manifest:
    script_name = os.path.basename(script_path)
    log_path = os.path.join(log_dir, f"{script_name}.log")
    print(f"▶ Running {script_path}")

    try:
        # Run script and capture both stdout and stderr
        result = subprocess.run(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(result.stdout)
            log_file.write(result.stderr)

        if result.returncode == 0:
            summary_lines.append(f"{script_name}\tPASS\t-")
            print(f"✅ Success: {script_name}")
        else:
            error_type = "UnknownError"
            if "FileNotFoundError" in result.stderr:
                error_type = "FileNotFoundError"
            elif "ImportError" in result.stderr:
                error_type = "ImportError"
            elif "ModuleNotFoundError" in result.stderr:
                error_type = "ModuleNotFoundError"
            elif "UnicodeEncodeError" in result.stderr:
                error_type = "UnicodeEncodeError"
            summary_lines.append(f"{script_name}\tFAIL\t{error_type}")
            print(f"❌ Error in {script_name}")

    except Exception as e:
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(str(e))
        summary_lines.append(f"{script_name}\tFAIL\tRunnerException")
        print(f"❌ Runner failed for {script_name}: {e}")

# Save final summary
with open(summary_file, "w", encoding="utf-8") as sf:
    sf.write("\n".join(summary_lines))

print(f"\n📜 Run complete. Summary saved to {summary_file}")
