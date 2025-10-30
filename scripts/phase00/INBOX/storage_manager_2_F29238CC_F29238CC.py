# -*- coding: utf-8 -*-
import os
import logging


class StorageManager:
    def __init__(self, base_path="data"):
        self.base_path = base_path

    def ensure_folder(self, folder_name):
        path = os.path.join(self.base_path, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"âœ… Created folder: {path}")
            logging.info(f"Created folder: {path}")
        else:
            print(f"â„¹ï¸ Folder already exists: {path}")
            logging.info(f"Folder already exists: {path}")


__all__ = ["StorageManager"]
