import os
import subprocess
import csv
from pathlib import Path

# === CONFIG ===
PHASE_11_DIR = Path("scripts/phase11")
OUTPUT_LOG = Path("outputs/logs/phase11_sanity_report.csv")

# Ensure output directory exists
OUTPUT_LOG.parent.mkdir(parents=True, exist_ok=True)

results = []

print("\n🚀 Starting Phase 11 Sanity Test Scan...")

for root, dirs, files in os.walk(PHASE_11_DIR):
    for file in files:
        if file.endswith("_READY.py"):
            file_path = Path(root) / file
            status = "✅ PASS"
            error_message = ""

            try:
                # Detect placeholder by file size or placeholder text
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if len(content.strip()) < 20 or "Placeholder" in content:
                    status = "⏳ Placeholder"
                else:
                    # Run script safely
                    result = subprocess.run([
                        "python", str(file_path)
                    ], capture_output=True, text=True, timeout=15)

                    if result.returncode != 0:
                        status = "❌ FAIL"
                        error_message = result.stderr.strip() or result.stdout.strip()

            except Exception as e:
                status = "❌ FAIL"
                error_message = str(e)

            results.append([file, status, error_message])
            print(f"{status} → {file}")

# Write results to CSV
with open(OUTPUT_LOG, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Script Name", "Status", "Error Message"])
    writer.writerows(results)

print(f"\n📄 Sanity test completed. Report saved to: {OUTPUT_LOG}")
