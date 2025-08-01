#!/usr/bin/env python3
"""
MAGIC Project – File Watchdog Agent
-----------------------------------
Purpose:
- Monitor key MAGIC directories for any file changes
- Detect new, deleted, or moved files
- Log all events to magic_master_log.txt for audit and awareness

Author: ChatGPT Assistant
"""

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===== CONFIGURATION =====
WATCH_PATHS = [
    "D:\\MAGIC\\inbox",
    "D:\\MAGIC\\review",
    "D:\\MAGIC\\approved",
    "D:\\MAGIC\\hold",
    "D:\\MAGIC\\quarantine",
    "D:\\MAGIC\\scripts"
]
LOG_FILE = "D:\\MAGIC\\logs\\magic_master_log.txt"


class MagicEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.log_event("🆕 Created", event.src_path)

    def on_deleted(self, event):
        self.log_event("❌ Deleted", event.src_path)

    def on_moved(self, event):
        self.log_event("📂 Moved", f"{event.src_path} -> {event.dest_path}")

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("✏️ Modified", event.src_path)

    def log_event(self, action, path):
        log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {action}: {path}\n"
        print(log_entry.strip())
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)


if __name__ == "__main__":
    print("🔍 MAGIC File Watchdog Agent started...")
    observer = Observer()
    handler = MagicEventHandler()

    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)
        else:
            print(f"⚠️ Skipping missing path: {path}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
