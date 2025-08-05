import json
import subprocess
import os

with open("phase_manifest.json", encoding="utf-8-sig") as f:
    manifest = json.load(f)

for script in manifest:
    if not os.path.isfile(script):
        print(f"⚠️ Skipping missing: {script}")
        continue
    print(f"▶ Running {script}")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error in {script}")
