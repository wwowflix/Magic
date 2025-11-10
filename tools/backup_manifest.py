import os
import shutil
import time

os.makedirs("outputs/manifest_backups", exist_ok=True)
src = "phase_manifest.json"
dst = f"outputs/manifest_backups/manifest_backup_{int(time.time())}.json"
if os.path.exists(src):
    shutil.copy2(src, dst)
    print("Backed up to", dst)
else:
    print("phase_manifest.json not found")
