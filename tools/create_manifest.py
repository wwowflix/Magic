import os
import json

manifest = []

for root, dirs, files in os.walk("scripts"):
    for file in files:
        if file.endswith("_READY.py"):
            parts = root.split(os.sep)
            if len(parts) >= 3:
                phase_part = parts[1]  # like phase11
                module_part = parts[2]  # like module_A
                try:
                    phase_number = int(phase_part.replace("phase", ""))
                except:
                    continue
                entry = {
                    "Phase": phase_number,
                    "Module": module_part.replace("module_", "").upper(),
                    "FinalFilename": os.path.join(root, file).replace("\\", "/")
                }
                manifest.append(entry)

with open("phase_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"✅ Manifest created with {len(manifest)} scripts.")
