import os
import pandas as pd

csv_path = "outputs/notion_export/magic_patch.csv"
df = pd.read_csv(csv_path)

print("📋 Columns found in CSV:", list(df.columns))

# Try fallback if FullPath is not present
if "FullPath" in df.columns:
    paths_to_check = df["FullPath"].dropna().tolist()
else:
    # Build full path manually from parts
    print("🔧 Rebuilding paths from Phase, Module, and Filename...")
    base_dir = "D:/MAGIC/scripts"
    paths_to_check = []

    for _, row in df.iterrows():
        phase = f"phase{int(row['Phase']):02}"
        module = f"module_{str(row['Module']).upper()}"
        filename = row["Filename"]
        full_path = os.path.join(base_dir, phase, module, filename)
        paths_to_check.append(full_path)

missing_files = [p for p in paths_to_check if not os.path.exists(p)]

if not missing_files:
    print("✅ All expected scripts are present.")
else:
    print(f"❌ Missing {len(missing_files)} files:")
    for p in missing_files:
        print(f" - {p}")
