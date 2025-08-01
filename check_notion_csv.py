import pandas as pd

# Path to your CSV export file from Notion
notion_csv_path = r"D:\MAGIC\magic_file_tracker_export.csv"

# Load CSV into DataFrame
df = pd.read_csv(notion_csv_path)

# Show a quick summary
print(f"Loaded {len(df)} entries from Notion CSV.")
print(df.head())

# Optionally save a clean snapshot CSV for backup
df.to_csv(r"D:\MAGIC\notion_snapshot_clean.csv", index=False)
