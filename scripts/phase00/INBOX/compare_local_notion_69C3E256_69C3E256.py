import os
import pandas as pd

# Paths
local_scripts_dir = r"D:\MAGIC\scripts"  # Your local scripts root folder
notion_csv_path = r"C:\\temp\\magic_file.csv"

# Load Notion CSV
notion_df = pd.read_csv(notion_csv_path)

# Get all local script filenames (recursive)
local_files = []
for root, dirs, files in os.walk(local_scripts_dir):
    for file in files:
        if file.endswith(".py"):
            local_files.append(file)

local_files_set = set(local_files)
notion_files_set = set(notion_df["Filename"].dropna())

# Find scripts in local but missing in Notion
missing_in_notion = local_files_set - notion_files_set

# Find scripts in Notion but missing locally
missing_locally = notion_files_set - local_files_set

print(f"Scripts missing in Notion: {len(missing_in_notion)}")
for f in sorted(missing_in_notion):
    print(f"  - {f}")

print(f"\nScripts missing locally: {len(missing_locally)}")
for f in sorted(missing_locally):
    print(f"  - {f}")
