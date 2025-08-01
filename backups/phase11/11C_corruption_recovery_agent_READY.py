import os
import shutil
import zipfile

# CONFIG
BACKUP_DIR = 'backups/'
SCRIPT_ROOT = 'scripts/'

def find_latest_backup():
    backups = sorted([
        f for f in os.listdir(BACKUP_DIR)
        if f.endswith('.zip')
    ], reverse=True)
    return os.path.join(BACKUP_DIR, backups[0]) if backups else None

def is_corrupted(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return False
    except Exception:
        return True

corrupted_files = []
for root, _, files in os.walk(SCRIPT_ROOT):
    for file in files:
        if file.endswith('.py'):
            full_path = os.path.join(root, file)
            if is_corrupted(full_path):
                corrupted_files.append(full_path)

if not corrupted_files:
    print('✅ No corrupted files found.')
else:
    print(f'❌ Found {len(corrupted_files)} corrupted files. Attempting restore...')
    latest_backup = find_latest_backup()
    if not latest_backup:
        print('⚠️ No backup found. Cannot restore.')
    else:
        with zipfile.ZipFile(latest_backup, 'r') as zip_ref:
            for corrupt in corrupted_files:
                arcname = os.path.relpath(corrupt, start=os.path.dirname(SCRIPT_ROOT))
                if arcname in zip_ref.namelist():
                    zip_ref.extract(arcname, path='.')
                    print(f'🔁 Restored: {corrupt}')
                else:
                    print(f'⚠️ Not found in backup: {corrupt}')
