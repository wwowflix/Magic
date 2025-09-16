import os
import time
import hashlib
from datetime import datetime

WATCH_DIRS = ["inbox", "scripts"]
STATE_FILE = "agents/awareness/script_tracker_state.json"
CHECK_INTERVAL = 60  # seconds

import json


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def file_hash(path):
    hasher = hashlib.md5()
    try:
        with open(path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None


def scan_files(state):
    changed = []
    current_state = {}

    for base_dir in WATCH_DIRS:
        if not os.path.exists(base_dir):
            continue
        for root, _, files in os.walk(base_dir):
            for file in files:
                if not file.endswith(".py"):
                    continue
                path = os.path.join(root, file)
                h = file_hash(path)
                current_state[path] = h

                if path not in state or state[path] != h:
                    changed.append(path)

    return changed, current_state


def main():
    print("▶ Starting Script Tracker. Ctrl+C to stop.")
    state = load_state()

    while True:
        changed, current_state = scan_files(state)
        if changed:
            print(f"📝 Detected {len(changed)} new/modified scripts:")
            for script in changed:
                print(f" - {script}")
        else:
            print(f"✅ No script changes detected at {datetime.now()}")
        state = current_state
        save_state(state)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
