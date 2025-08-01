import os
import shutil
import pandas as pd

CSV_PATH = "outputs/notion_export/magic_patch.csv"
BACKUP_DIR = "backups/"
restored = 0

if not os.path.exists(CSV_PATH):
    print("❌ CSV file not found at", CSV_PATH)
    exit()

df = pd.read_csv(CSV_PATH)
for idx, row in df.iterrows():
    try:
        full_path = row["FullPath"]
        if not os.path.exists(full_path):
            filename = os.path.basename(full_path)
            backup_path = os.path.join(BACKUP_DIR, filename)
            if os.path.exists(backup_path):
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                shutil.copy2(backup_path, full_path)
                print(f"✅ Restored: {filename}")
                restored += 1
            else:
                print(f"⚠️ Missing in backup: {filename}")
    except Exception as e:
        print("❌ Error:", e)

if restored == 0:
    print("✅ No files to restore.")
else:
    print(f"🔁 Total restored files: {restored}")
