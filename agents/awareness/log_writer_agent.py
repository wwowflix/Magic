#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import time

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "magic.log"


def ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    ensure_log_dir()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}\n"
    print(line.strip())
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line)


def main() -> None:
    log("Log writer agent ready.")


if __name__ == "__main__":
    main()
