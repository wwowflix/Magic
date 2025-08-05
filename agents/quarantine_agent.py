import os
import shutil
import json
import re

QUARANTINE_DIR = 'quarantine'
SCRIPT_MAP_PATH = 'script_name_to_path.json'
LOGS_DIR = os.path.join('outputs', 'logs')

def is_corrupted(log_file_path):
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except UnicodeDecodeError:
        with open(log_file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore').lower()
    return any(err in content for err in ['traceback', 'error', 'exception'])

def extract_script_name(log_filename):
    name = log_filename
    if name.endswith('.log'):
        name = name[:-4]
    name = re.sub(r'_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', '', name)
    if not name.endswith('.py'):
        name += '.py'
    return name

def quarantine_script(script_path):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    dest_path = os.path.join(QUARANTINE_DIR, os.path.basename(script_path))
    shutil.move(script_path, dest_path)
    print(f"🛑 Quarantined script: {script_path} → {dest_path}")

def main():
    with open(SCRIPT_MAP_PATH, 'r', encoding='utf-8') as f:
        script_map = json.load(f)

    for root, _, files in os.walk(LOGS_DIR):
        for file in files:
            if not file.endswith('.log'):
                continue
            log_path = os.path.join(root, file)
            if is_corrupted(log_path):
                script_name = extract_script_name(file)
                script_path = script_map.get(script_name)
                if script_path and os.path.exists(script_path):
                    quarantine_script(script_path)
                else:
                    print(f"⚠️ Script not found or missing in map: {script_name}")

if __name__ == "__main__":
    main()
