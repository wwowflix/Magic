# storage_manager.py

import os
import logging

logging.basicConfig(filename="orchestrator.log", level=logging.DEBUG)


class StorageManager:
    def __init__(self, base_path="data"):
        self.base_path = base_path

    def ensure_folder(self, folder_name):
        path = os.path.join(self.base_path, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Created folder: {path}")
            logging.info(f"Created folder: {path}")
        else:
            print(f"ℹ️ Folder already exists: {path}")
            logging.info(f"Folder already exists: {path}")

    def check_missing_folders(self, folders):
        missing = []
        for f in folders:
            path = os.path.join(self.base_path, f)
            if not os.path.exists(path):
                missing.append(f)
        logging.info(f"Checked missing folders. Missing: {missing}")
        return missing


if __name__ == "__main__":
    sm = StorageManager()
    folders_needed = ["inputs", "outputs", "logs", "temp"]
    missing = sm.check_missing_folders(folders_needed)
    if missing:
        for f in missing:
            sm.ensure_folder(f)
    else:
        print("✅ All folders exist.")
