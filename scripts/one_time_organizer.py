#!/usr/bin/env python3
"""
One-Time Organizer: Bulk-moves project files into canonical folders

Rules:
  - *.py         → scripts/
  - *.md         → docs/
  - *reddit*.csv → outputs/trends/
  - *.csv        → outputs/data/
  - *.log        → logs/archive/

Skips:
  - venv/
  - .git/
  - outputs/data, outputs/trends, logs/archive (already-sorted)
"""
import sys
import os

# 1) Locate this script's directory (or fall back)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

# 2) Remove it from sys.path so local modules can't shadow stdlib
if sys.path and sys.path[0] == script_dir:
    sys.path.pop(0)

# 3) Now it's safe to import stdlib
import shutil
import logging

# 4) Determine project root (one level up)
BASE_DIR = os.path.abspath(os.path.join(script_dir, ".."))

# 5) Define your move rules
action_rules = [
    (lambda fn: fn.endswith('.py'),
        os.path.join(BASE_DIR, 'scripts')),
    (lambda fn: fn.endswith('.md'),
        os.path.join(BASE_DIR, 'docs')),
    (lambda fn: fn.lower().endswith('.csv') and 'reddit' in fn.lower(),
        os.path.join(BASE_DIR, 'outputs', 'trends')),
    (lambda fn: fn.lower().endswith('.csv'),
        os.path.join(BASE_DIR, 'outputs', 'data')),
    (lambda fn: fn.lower().endswith('.log'),
        os.path.join(BASE_DIR, 'logs', 'archive')),
]

def should_skip(path: str) -> bool:
    """Skip virtualenv, git metadata, and already-organized folders."""
    exclude = [
        'venv', '.git',
        os.path.join('outputs', 'data'),
        os.path.join('outputs', 'trends'),
        os.path.join('logs', 'archive'),
    ]
    return any(seg in path for seg in exclude)

def organize():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info(f"Organizing files in {BASE_DIR}...")
    for root, dirs, files in os.walk(BASE_DIR):
        if should_skip(root):
            continue
        for fname in files:
            for match_fn, dest_dir in action_rules:
                if match_fn(fname):
                    src = os.path.join(root, fname)
                    dst = os.path.join(dest_dir, fname)
                    # already in place?
                    if os.path.abspath(src) == os.path.abspath(dst):
                        break
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(src, dst)
                    logging.info(f"Moved {src} → {dst}")
                    break
    logging.info("Done.")

if __name__ == "__main__":
    organize()
