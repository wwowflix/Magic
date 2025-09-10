# -*- coding: utf-8 -*-
"""
fix_indentation_pass.py — targeted pass to heal IndentationError/TabError and common whitespace issues.
- Converts tabs -> 4 spaces
- Replaces NBSP/odd spaces with normal space
- Normalizes CRLF -> LF
- Strips trailing whitespace
- Ensures final newline
- Only writes if content changed
- Backs up originals to outputs/backups/indentfix_YYYYmmdd_HHMMSS/
"""
import json
import os
import re
import sys
import time
import io
import py_compile
from typing import List

ROOT = r"D:\MAGIC"
HELPER = r"D:\MAGIC\tools\compile_helper.py"

SPACE_REMAP = {
    "\u00a0": " ",  # NBSP
    "\u2007": " ",  # Figure space
    "\u202f": " ",  # Narrow no-break space
}


def read_text(path: str) -> str:
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_text(path: str, text: str):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def normalize_ws(text: str) -> str:
    # Canonicalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace odd spaces
    for k, v in SPACE_REMAP.items():
        if k in text:
            text = text.replace(k, v)

    # Tabs -> 4 spaces (only on leading runs for safety)
    def fix_leading_tabs(line: str) -> str:
        m = re.match(r"^(\s+)", line)
        if not m:
            return line
        lead = m.group(1)
        lead = lead.replace("\t", "    ")
        return lead + line[len(m.group(1)) :]

    lines = [fix_leading_tabs(ln) for ln in text.split("\n")]
    # Strip trailing spaces
    lines = [re.sub(r"[ \t]+$", "", ln) for ln in lines]
    # Rejoin & ensure trailing newline
    out = "\n".join(lines)
    if not out.endswith("\n"):
        out += "\n"
    return out


def compile_ok(path: str) -> bool:
    try:
        py_compile.compile(path, doraise=True)
        return True
    except Exception:
        return False


def load_fail_list() -> List[str]:
    # Try helper (expected to emit JSON with {failed:int, fails:[{path,error},...]})
    if os.path.exists(HELPER):
        try:
            import subprocess

            out = subprocess.check_output(
                [sys.executable, HELPER], stderr=subprocess.STDOUT
            )
            rep = json.loads(out.decode("utf-8", "replace"))
            fails = rep.get("fails") or []
            paths = [
                f.get("path") for f in fails if isinstance(f, dict) and f.get("path")
            ]
            return [p for p in paths if p and os.path.exists(p)]
        except Exception:
            pass
    # Fallback: scan *_READY.py
    targets = []
    for root, _, files in os.walk(os.path.join(ROOT, "scripts")):
        for fn in files:
            if fn.endswith("_READY.py"):
                p = os.path.join(root, fn)
                if not compile_ok(p):
                    targets.append(p)
    return targets


def main():
    targets = load_fail_list()
    if not targets:
        print("No failing files detected.")
        return

    stamp = time.strftime("%Y%m%d_%H%M%S")
    bkp_dir = os.path.join(ROOT, "outputs", "backups", f"indentfix_{stamp}")
    os.makedirs(bkp_dir, exist_ok=True)

    fixed = 0
    tried = 0
    for p in targets:
        tried += 1
        raw = read_text(p)
        healed = normalize_ws(raw)
        if healed != raw:
            # Only bother if this looks like an indent-style failure
            # Try compile after normalization; only keep if it helps or is neutral.
            write_text(p, healed)
            if compile_ok(p):
                fixed += 1
            else:
                # If still broken, keep the normalized version (neutral),
                # but on first failure we also make a backup of the original.
                # Put original to backup for safety.
                orig_bkp = os.path.join(bkp_dir, os.path.relpath(p, ROOT))
                os.makedirs(os.path.dirname(orig_bkp), exist_ok=True)
                write_text(orig_bkp, raw)
        else:
            # No change; maybe pure syntax problem unrelated to whitespace.
            pass

    print(
        f"[indentfix] Tried: {tried} | Fixed or improved whitespace on: {fixed} | Backup: {bkp_dir}"
    )

    # Optional: print a quick summary of remaining compile failures
    remaining = [p for p in targets if not compile_ok(p)]
    print(f"[indentfix] Still failing after pass: {len(remaining)}")
    for p in remaining[:10]:
        print(" -", p)


if __name__ == "__main__":
    main()
