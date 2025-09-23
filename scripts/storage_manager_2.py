# -*- coding: utf-8 -*-
import os
import logging


class StorageManager:
    def __init__(self):
        logging.info("StorageManager initialized.")

    def ensure_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Folder created: {folder_path}")
        else:
            logging.info(f"Folder already exists: {folder_path}")


__all__ = ["StorageManager"]
