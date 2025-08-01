import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDERS = [
    "D:/MAGIC/inbox/",
    "D:/MAGIC/review/",
    "D:/MAGIC/approved/",
    "D:/MAGIC/scripts/",
    "D:/MAGIC/quarantine/"
]

LOG_FILE = "logs/file_watchdog.log"

class WatchdogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f"Modified: {event.src_path}")

    def on_created(self, event):
        logging.info(f"Created: {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"Deleted: {event.src_path}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

    observer = Observer()
    for folder in WATCHED_FOLDERS:
        observer.schedule(WatchdogHandler(), folder, recursive=True)
        logging.info(f"Watching folder: {folder}")

    observer.start()
    print("👁️ Watching for file changes... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
