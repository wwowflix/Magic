import subprocess
import datetime
import os
import sys

# ----------------------------
# CONFIGURATION
# ----------------------------
PROJECT_ROOT = r"D:\MAGIC"
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
LOG_DIR = os.path.join(PROJECT_ROOT, "outputs", "logs")
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
CYCLE_LOG = os.path.join(LOG_DIR, f"phase11_cycle_log_{TIMESTAMP}.txt")

AUTOHEAL_SCRIPT = os.path.join(TOOLS_DIR, "magic_phase11_autoheal_and_test.ps1")
ORCHESTRATOR_SCRIPT = os.path.join(TOOLS_DIR, "Magic_Orchestrator_Master_FIXED.ps1")
NOTION_PATCHER = os.path.join(PROJECT_ROOT, "notion_status_patcher_FIXED.py")


# ----------------------------
# Helpers
# ----------------------------
def run_command(command, step_name):
    """Runs a shell command and logs its output."""
    print(f"\n▶ {step_name}...")
    with open(CYCLE_LOG, "a", encoding="utf-8") as log:
        log.write(f"\n=== {step_name} ===\n")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            log.write(result.stdout.decode("utf-8", errors="ignore"))
            print(f"✅ {step_name} completed.")
        except subprocess.CalledProcessError as e:
            log.write(e.stdout.decode("utf-8", errors="ignore"))
            print(f"❌ {step_name} failed. Check log for details.")


# ----------------------------
# MAIN EXECUTION
# ----------------------------
def main():
    print("=" * 40)
    print("MAGIC PROJECT – PHASE 11 FULL CYCLE")
    print("=" * 40)
    print(f"Log File: {CYCLE_LOG}")

    os.makedirs(LOG_DIR, exist_ok=True)

    # 1️⃣ Auto-Heal
    run_command(
        f'powershell -ExecutionPolicy Bypass -File "{AUTOHEAL_SCRIPT}"',
        "STEP 1: Auto-Heal Placeholders",
    )

    # 2️⃣ Master Orchestrator
    run_command(
        f'powershell -ExecutionPolicy Bypass -File "{ORCHESTRATOR_SCRIPT}"',
        "STEP 2: Run Master Orchestrator",
    )

    # 3️⃣ Notion Sync
    run_command(f'"{sys.executable}" "{NOTION_PATCHER}"', "STEP 3: Patch Notion Tracker")

    print("\n=============================")
    print(" ✅ PHASE 11 FULL CYCLE COMPLETED")
    print(f" 📜 Log saved to: {CYCLE_LOG}")
    print("=============================\n")


if __name__ == "__main__":
    main()
