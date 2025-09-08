import os
import shutil
from datetime import datetime

BACKUP_DIR = "backups"


def backup_file(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist, skipping backup.")
        return
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(filepath)
    backup_name = f"{base_name}_{timestamp}.bak"
    dest = os.path.join(BACKUP_DIR, backup_name)
    print(f"Backing up {filepath} to {dest}")
    shutil.copy2(filepath, dest)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python backup_agent.py <file_path>")
        sys.exit(1)
    backup_file(sys.argv[1])
