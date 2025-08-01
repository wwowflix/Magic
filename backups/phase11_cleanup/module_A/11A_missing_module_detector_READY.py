import os
import pandas as pd

# Config
PATCH_CSV_PATH = "outputs/notion_export/magic_patch.csv"
LOG_OUTPUT = "outputs/logs/missing_scripts_report.txt"

# Load the expected script list
df = pd.read_csv(PATCH_CSV_PATH)

# Only include scripts marked _READY and with a valid path
ready_scripts = df[df["Filename"].str.endswith("_READY.py")]
ready_scripts = ready_scripts.dropna(subset=["Path"])

missing_files = []

for _, row in ready_scripts.iterrows():
    path_value = row["Path"]
    if isinstance(path_value, str):
        expected_path = os.path.normpath(path_value)
        if not os.path.exists(expected_path):
            missing_files.append(f'{row["Phase"]} | {row["Module"]} | {row["Filename"]} → MISSING')

# Output to log file
os.makedirs(os.path.dirname(LOG_OUTPUT), exist_ok=True)

with open(LOG_OUTPUT, "w", encoding="utf-8") as f:
    if not missing_files:
        f.write("✅ All expected scripts are present.\n")
    else:
        f.write("❌ Missing Scripts Detected:\n")
        for entry in missing_files:
            f.write(f"{entry}\n")

print(f"🔍 Scan complete. Missing entries: {len(missing_files)}")
print(f"📄 See report: {LOG_OUTPUT}")
