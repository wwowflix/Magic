# Scans scripts/phase*/**/*_READY.py and writes audit_list.txt
import os
import glob
import pathlib

root = r"D:\MAGIC"
out = os.path.join(root, "audit_list.txt")
paths = sorted(
    glob.glob(
        os.path.join(root, "scripts", "phase*", "**", "*_READY.py"), recursive=True
    )
)
with open(out, "w", encoding="utf-8") as f:
    for p in paths:
        # keep repo-relative for readability
        rel = (
            pathlib.Path(p).as_posix().replace(pathlib.Path(root).as_posix() + "/", "")
        )
        f.write(rel + "\n")
print(f"Wrote {out} ({len(paths)} items)")
