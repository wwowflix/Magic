# tools/self_heal_agents.py
from __future__ import annotations
import os, shutil, time

def _ts() -> str: return time.strftime("%Y%m%d_%H%M%S")
def _mkdir(p: str) -> None: os.makedirs(p, exist_ok=True)

def backup_file(abs_path: str, root: str, backups_root: str) -> str:
    rel = os.path.relpath(abs_path, root)
    dst = os.path.join(backups_root, _ts(), rel)
    _mkdir(os.path.dirname(dst)); shutil.copy2(abs_path, dst); return dst

def quarantine_file(abs_path: str, root: str, quarantine_root: str) -> str:
    rel = os.path.relpath(abs_path, root)
    dst = os.path.join(quarantine_root, _ts(), rel)
    _mkdir(os.path.dirname(dst)); shutil.move(abs_path, dst); return dst

def create_placeholder(abs_path: str) -> None:
    _mkdir(os.path.dirname(abs_path))
    if not os.path.exists(abs_path):
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(
                "# AUTO-GENERATED PLACEHOLDER\n"
                "import sys\n"
                "print('[placeholder] running:', __file__)\n"
                "sys.exit(0)\n"
            )
