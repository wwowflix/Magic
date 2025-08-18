import os
import shutil
import sys
from datetime import datetime

BACKUP_BASE = "backups"


def backup_file(file_path):
    if not os.path.isfile(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False

    # Create backups folder if missing
    os.makedirs(BACKUP_BASE, exist_ok=True)

    # Normalize paths for consistent folder structure inside backups
    abs_file_path = os.path.abspath(file_path)
    base_dir = os.path.abspath("scripts")  # Root of scripts folder
    try:
        rel_path = os.path.relpath(abs_file_path, base_dir)
    except ValueError:
        # File outside scripts folder; just use filename
        rel_path = os.path.basename(file_path)

    # Create destination backup folder path
    dest_folder = os.path.join(BACKUP_BASE, os.path.dirname(rel_path))
    os.makedirs(dest_folder, exist_ok=True)

    # Create timestamped backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = os.path.basename(file_path)
    backup_name = f"{base_name}_{timestamp}.bak"
    backup_path = os.path.join(dest_folder, backup_name)

    # Copy file
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backed up {file_path} to {backup_path}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup_agent.py <file_path_to_backup>")
        sys.exit(1)
    file_to_backup = sys.argv[1]
    backup_file(file_to_backup)
