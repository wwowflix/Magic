# generate_manifest.py
import os
import json

# Adjust if your scripts live somewhere else
ROOT = os.path.join(os.getcwd(), "scripts")

manifest = {}
for phase in sorted(os.listdir(ROOT)):
    phase_dir = os.path.join(ROOT, phase)
    if not os.path.isdir(phase_dir) or not phase.startswith("phase"):
        continue

    modules = {}
    for module in sorted(os.listdir(phase_dir)):
        mod_dir = os.path.join(phase_dir, module)
        if not os.path.isdir(mod_dir):
            continue

        ready_files = sorted(f for f in os.listdir(mod_dir) if f.endswith("_READY.py"))
        modules[module] = ready_files

    manifest[phase] = modules

with open("phase_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Wrote phase_manifest.json")
