import json
import subprocess
import sys
from pathlib import Path

# --- Load Manifest ---
manifest_file = sys.argv[1] if len(sys.argv) > 1 else "phase_manifest.json"
with open(manifest_file, encoding="utf-8-sig") as f:
    scripts = json.load(f)

# --- Setup output folders ---
logs_dir = Path("outputs/logs")
summaries_dir = Path("outputs/summaries")
logs_dir.mkdir(parents=True, exist_ok=True)
summaries_dir.mkdir(parents=True, exist_ok=True)

summary_file = summaries_dir / "self_healing_summary.tsv"

# --- Runner Loop ---
results = []
for script in scripts:
    script_path = Path(script)
    log_path = logs_dir / f"{script_path.stem}.log"
    print(f"▶ Running {script}")

    try:
        proc = subprocess.run(
            ["python", script], capture_output=True, text=True, timeout=30
        )
        with open(log_path, "w", encoding="utf-8") as log:
            log.write(proc.stdout)
            log.write(proc.stderr)

        if proc.returncode == 0:
            results.append((script, "PASS", ""))
        else:
            results.append(
                (
                    script,
                    "FAIL",
                    (
                        proc.stderr.strip().splitlines()[-1]
                        if proc.stderr
                        else "Unknown Error"
                    ),
                )
            )

    except subprocess.TimeoutExpired:
        results.append((script, "FAIL", "Timeout"))
    except Exception as e:
        results.append((script, "FAIL", f"RunnerError: {str(e)}"))

# --- Write Summary ---
with open(summary_file, "w", encoding="utf-8") as s:
    s.write("Script\tStatus\tError\n")
    for script, status, error in results:
        s.write(f"{script}\t{status}\t{error}\n")

print(f"✅ Completed {len(results)} scripts. Summary saved to {summary_file}")
