import os
import zipfile
from datetime import datetime

# CONFIG
FOLDERS_TO_BACKUP = [
    'scripts/',
    'outputs/data/',
    'outputs/trends/',
    'configs/',
    'docs/'
]
BACKUP_DIR = 'backups/'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_filename = f'backup_{timestamp}.zip'
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Ensure backup folder exists
os.makedirs(BACKUP_DIR, exist_ok=True)

# Create ZIP archive
with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
    for folder in FOLDERS_TO_BACKUP:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=os.path.dirname(folder))
                backup_zip.write(full_path, arcname)

print(f"✅ Backup created: {backup_path}")
