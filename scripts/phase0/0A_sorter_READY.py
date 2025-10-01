"""
Phase 0A – Sorter Script
Moves files from inbox to scripts\phase{NN}\module_{A..Z} based on names like 03C_task_READY.py
"""
import os, re, shutil, sys

ROOT    = r"D:\MAGIC"
INBOX   = os.path.join(ROOT, "inbox")
SCRIPTS = os.path.join(ROOT, "scripts")

pat = re.compile(r"^(?P<phase>\d{2})(?P<module>[A-Z])_.*_READY\.py$")

def log(msg): print(msg) if "--verbose" in sys.argv else None

def main():
    if not os.path.exists(INBOX):
        print("Inbox missing, nothing to process."); return
    for fname in os.listdir(INBOX):
        fpath = os.path.join(INBOX, fname)
        if not os.path.isfile(fpath): continue
        m = pat.match(fname)
        if not m: 
            log(f"skip: {fname}")
            continue
        phase = f"phase{int(m.group('phase'))}"
        module = f"module_{m.group('module')}"
        dest_dir = os.path.join(SCRIPTS, phase, module)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, fname)
        shutil.move(fpath, dest)
        print(f"moved: {fname} -> {phase}\\{module}")

if __name__ == "__main__":
    main()
