import os
import shutil
import json
import re

QUARANTINE_DIR = "quarantine"
SCRIPT_MAP_PATH = "script_name_to_path.json"
LOGS_DIR = os.path.join("outputs", "logs")


def is_corrupted(log_file_path):
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
    except UnicodeDecodeError:
        with open(log_file_path, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore").lower()
    return any(err in content for err in ["traceback", "error", "exception"])


def normalize_script_name(log_path, log_file):
    # Remove .log
    name = log_file
    if name.endswith(".log"):
        name = name[:-4]

    # Remove trailing timestamps (both date and time formats)
    name = re.sub(r"_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$", "", name)
    name = re.sub(r"_\d{2}-\d{2}-\d{2}$", "", name)

    # Remove any trailing parts after '.py' in folder names (nested logs issue)
    # e.g. folder named '11A_error_log_monitor_READY.py' contains logs - remove trailing '.py' folder name
    # Also flatten: if log is inside a folder with script name + '.py', just use that base script name
    parent_folder = os.path.basename(os.path.dirname(log_path))
    if parent_folder.endswith(".py"):
        name = parent_folder

    # If name ends with '.py.py' fix double suffix
    if name.endswith(".py.py"):
        name = name[:-3]

    # Ensure ends with .py
    if not name.endswith(".py"):
        name += ".py"

    return name


def quarantine_script(script_path):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    dest_path = os.path.join(QUARANTINE_DIR, os.path.basename(script_path))
    shutil.move(script_path, dest_path)
    print(f"🛑 Quarantined script: {script_path} → {dest_path}")


def main():
    with open(SCRIPT_MAP_PATH, "r", encoding="utf-8") as f:
        script_map = json.load(f)

    print(f"🔍 Loaded {len(script_map)} scripts in map.")

    for root, _, files in os.walk(LOGS_DIR):
        for file in files:
            if not file.endswith(".log"):
                continue

            log_path = os.path.join(root, file)
            if is_corrupted(log_path):
                normalized_name = normalize_script_name(log_path, file)

                script_path = script_map.get(normalized_name)
                if not script_path:
                    # Also try lowercase key (in case)
                    script_path = script_map.get(normalized_name.lower())

                if script_path and os.path.exists(script_path):
                    quarantine_script(script_path)
                else:
                    print(f"⚠️ Script not found or missing in map: {normalized_name}")


if __name__ == "__main__":
    main()
