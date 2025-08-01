import os
import csv

PHASE_DIR = 'scripts/phase11'
OUTPUT_CSV = 'sync/magic_patch.csv'

os.makedirs('sync', exist_ok=True)
entries = []

for root, _, files in os.walk(PHASE_DIR):
    for file in files:
        if file.endswith('_READY.py'):
            full_path = os.path.join(root, file)
            parts = full_path.replace("\\\\", "/").split('/')
            phase = "11"
            module = parts[-2].split('_')[-1].upper()
            status = "READY"
            entries.append({
                "Filename": file,
                "Phase": phase,
                "Module": module,
                "Status": status,
                "Folder": root.replace("\\\\", "/"),
                "Is Placeholder": "No",
                "Is Implemented": "Yes"
            })

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=entries[0].keys())
    writer.writeheader()
    writer.writerows(entries)

print(f"✅ Patch generated: {OUTPUT_CSV}")
