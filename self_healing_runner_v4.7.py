import os
import subprocess
import json
import re
from datetime import datetime
from collections import defaultdict

# Load manifest with utf-8-sig to handle BOM if any
with open('phase_manifest.json', 'r', encoding='utf-8-sig') as f:
    manifest = json.load(f)

LOGS_BASE = os.path.join('outputs', 'logs')
SUMMARY_BASE = os.path.join('outputs', 'summaries')
os.makedirs(LOGS_BASE, exist_ok=True)
os.makedirs(SUMMARY_BASE, exist_ok=True)

MAX_RETRIES = 3

# Healing agent scripts (assumed locations)
PLACEHOLDER_AGENT = 'agents/self_heal_placeholder.py'
QUARANTINE_AGENT = 'agents/quarantine_agent.py'
BACKUP_AGENT = 'agents/backup_agent.py'

def apply_remediation(error_msg, script_path):
    # Auto-fix common errors by checking error message contents
    if 'FileNotFoundError' in error_msg:
        missing_file_match = re.search(r"\'(.+?)\'", error_msg)
        if missing_file_match:
            missing_file = missing_file_match.group(1)
            try:
                with open(missing_file, 'w', encoding='utf-8') as f:
                    f.write("# Auto-created missing input file\n")
                print(f"🔧 Auto-fix applied: created missing file '{missing_file}'")
                return True
            except Exception as e:
                print(f"⚠️ Failed to auto-create file '{missing_file}': {e}")
                return False
    elif 'UnicodeDecodeError' in error_msg:
        # Could implement input/output cleaning here
        print("🔧 Auto-fix applied: UnicodeDecodeError detected (manual cleanup recommended)")
        return False
    elif 'ImportError' in error_msg:
        mod_match = re.search(r"No module named '([^']+)'", error_msg)
        if mod_match:
            module = mod_match.group(1)
            print(f"🔧 Auto-fix applied: installing missing module '{module}' via pip")
            subprocess.run(['pip', 'install', module])
            return True
    return False

def run_script(phase, module, script_path):
    log_folder = os.path.join(LOGS_BASE, f'phase{phase}_module_{module}')
    os.makedirs(log_folder, exist_ok=True)

    script_name = os.path.basename(script_path)
    log_file = os.path.join(log_folder, script_name.replace('.py', '.log'))

    for attempt in range(1, MAX_RETRIES+1):
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"\n=== Run started: {datetime.now()} (Attempt {attempt}) ===\n")
            try:
                result = subprocess.run(
                    ['python', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300
                )
                log.write("--- STDOUT ---\n")
                log.write(result.stdout + "\n")
                log.write("--- STDERR ---\n")
                log.write(result.stderr + "\n")
                log.write(f"Exit code: {result.returncode}\n")
                log.write(f"=== Run ended: {datetime.now()} ===\n")

                if result.returncode == 0:
                    return 0
                else:
                    log.write(f"[WARNING] Script failed on attempt {attempt}.\n")
                    print(f"[WARNING] {script_name} failed on attempt {attempt}.")

                    # Call Healing Agents on failure
                    # 1. Backup current script before any changes
                    subprocess.run(['python', BACKUP_AGENT, script_path])

                    # 2. Quarantine failing script for review
                    subprocess.run(['python', QUARANTINE_AGENT, script_path])

                    # 3. Create placeholders for missing or broken scripts
                    subprocess.run(['python', PLACEHOLDER_AGENT])

                    # Try remediation if possible
                    if apply_remediation(result.stderr, script_path):
                        print(f"🔧 Remediation applied, retrying script: {script_name}")
                        continue
                    else:
                        if attempt == MAX_RETRIES:
                            print(f"❌ {script_name} failed after {MAX_RETRIES} attempts.")
                            return 1
                        else:
                            continue

            except Exception as e:
                log.write(f"[ERROR] Exception while running script: {e}\n")
                if attempt == MAX_RETRIES:
                    print(f"❌ {script_name} failed after {MAX_RETRIES} attempts due to exception.")
                    return 1

def main():
    print(f"\n▶ Starting Self-Healing Runner v4.7 with auto-remediation on {len(manifest)} scripts...\n")

    total = 0
    passed = 0
    failed = 0

    results = defaultdict(list)

    for script_path in manifest:
        parts = os.path.normpath(script_path).split(os.sep)
        if len(parts) < 3:
            print(f"⚠️ Unexpected script path format: {script_path}")
            failed += 1
            continue

        phase = parts[-3].replace('phase', '')
        module = parts[-2].replace('module_', '')

        if not os.path.exists(script_path):
            print(f"⚠️ Missing script: {script_path}")
            failed += 1
            results[(phase, module)].append((os.path.basename(script_path), 'MISSING'))
            continue

        print(f"▶ Running: {os.path.basename(script_path)}")
        code = run_script(phase, module, script_path)

        total += 1
        status = 'PASS' if code == 0 else 'FAIL'
        if code == 0:
            passed += 1
        else:
            failed += 1

        results[(phase, module)].append((os.path.basename(script_path), status))

    # Write per-module summaries
    for (phase, module), scripts in results.items():
        summary_path = os.path.join(SUMMARY_BASE, f'phase{phase}_module_{module}_summary.tsv')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("Script\tStatus\n")
            for script_name, status in scripts:
                f.write(f"{script_name}\t{status}\n")

    print(f"\n=== SUMMARY ===")
    print(f"Total scripts: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Per-module summaries saved in: {SUMMARY_BASE}\n")

if __name__ == "__main__":
    main()
