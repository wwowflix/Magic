#!/usr/bin/env python3
from __future__ import annotations

import os
import time
from typing import Any

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except Exception:  # pragma: no cover
    # Allow type checking even if watchdog isn't installed at runtime
    class FileSystemEventHandler:  # type: ignore[no-redef]
        ...

    class Observer:  # type: ignore[no-redef]
        def schedule(self, *_: Any, **__: Any) -> None: ...
        def start(self) -> None: ...
        def stop(self) -> None: ...
        def join(self) -> None: ...


LOG_FILE = os.path.join(os.path.dirname(__file__), "file_watchdog.log")
WATCH_PATHS = [os.getcwd()]


class MagicEventHandler(FileSystemEventHandler):
    def on_created(self, event: Any) -> None:
        self.log_event("Created", event.src_path)

    def on_deleted(self, event: Any) -> None:
        self.log_event("Deleted", event.src_path)

    def on_moved(self, event: Any) -> None:
        self.log_event("Moved", f"{event.src_path} -> {event.dest_path}")

    def on_modified(self, event: Any) -> None:
        if not getattr(event, "is_directory", False):
            self.log_event("Modified", event.src_path)

    def log_event(self, action: str, path: str) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{ts}] {action}: {path}\n"
        print(log_entry.strip())
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)


def main() -> None:
    print("MAGIC File Watchdog Agent started...")
    observer = Observer()
    handler = MagicEventHandler()
    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)
        else:
            print(f"Skipping missing path: {path}")
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
