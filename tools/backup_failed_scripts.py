import os
import shutil
from datetime import datetime

SUMMARY_PATH = "outputs/summaries/phase_master_summary.tsv"
BACKUP_DIR = "backups/failed"

def read_failures(summary_path):
    failures = []
    if not os.path.exists(summary_path):
        print(f"❌ Summary file not found: {summary_path}")
        return failures

    with open(summary_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # skip header
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) >= 4 and parts[3] == "FAIL":
                phase, module, script, *_ = parts
                failures.append((phase, module, script))
    return failures

def find_script_path(phase, module, script):
    folder = f"scripts/phase{phase}/module_{module}"
    return os.path.join(folder, script)

def backup_script(script_path):
    if not os.path.exists(script_path):
        print(f"⚠️ Script not found: {script_path}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_name = os.path.basename(script_path)
    backup_subdir = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(backup_subdir, exist_ok=True)
    destination = os.path.join(backup_subdir, script_name)

    shutil.copy2(script_path, destination)
    print(f"📦 Backed up: {script_path} → {destination}")

def main():
    print("🔍 Scanning for failed scripts...")
    failed_entries = read_failures(SUMMARY_PATH)

    if not failed_entries:
        print("✅ No failed scripts found to back up.")
        return

    for phase, module, script in failed_entries:
        script_path = find_script_path(phase, module, script)
        backup_script(script_path)

    print(f"\n🗃️ Backup complete. All failed scripts stored in '{BACKUP_DIR}'.")

if __name__ == "__main__":
    main()
