import os
import shutil

# CONFIG
SEARCH_DIRS = ['.', 'configs/', 'settings/']
TARGET_DIR = 'configs/central_config_hub/'
ALLOWED_EXTENSIONS = ['.env', '.json', '.yaml', '.yml', '.ini', '.cfg']
LOG_FILE = 'outputs/logs/config_migration_log.txt'

moved_files = []

os.makedirs(TARGET_DIR, exist_ok=True)
for search_dir in SEARCH_DIRS:
    for root, _, files in os.walk(search_dir):
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                source = os.path.join(root, file)
                dest = os.path.join(TARGET_DIR, file)
                try:
                    if os.path.abspath(source) != os.path.abspath(dest):
                        shutil.copy2(source, dest)
                        moved_files.append(f"✅ Copied: {source} → {dest}")
                except Exception as e:
                    moved_files.append(f"⚠️ Error copying {source}: {e}")

# Log the operation
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    if moved_files:
        f.write("📦 Config migration log:\n" + "\n".join(moved_files))
    else:
        f.write("✅ No config files found to migrate.\n")

print(f"📁 Config migration complete. Log saved to: {LOG_FILE}")
