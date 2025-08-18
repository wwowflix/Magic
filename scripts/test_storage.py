import os
import logging
from storage_manager import StorageManager

log_path = r"D:\MAGIC\data\logs\storage_test.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

sm = StorageManager()
sm.ensure_folder(r"D:\MAGIC\data\test_folder")

print("Test complete. Check logs at D:\\MAGIC\\data\\logs\\storage_test.log")
