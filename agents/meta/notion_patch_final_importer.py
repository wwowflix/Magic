import os
import csv
from datetime import datetime
import pandas as pd
from notion_client import Client
from dotenv import load_dotenv

# === 1. Load Notion credentials ===
load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

# === 2. File path ===
patch_file_path = "outputs/notion_export/magic_patch.csv"

# === 3. Fix and clean CSV ===
df = pd.read_csv(patch_file_path)

# Ensure required columns exist
required_columns = ["Filename", "Phase", "Module", "Prefix", "Status", "Path", "Last Updated"]
for col in required_columns:
    if col not in df.columns:
        df[col] = ""

# Fill missing prefixes using first 4 characters of filename
df["Prefix"] = df["Prefix"].fillna("")
df.loc[df["Prefix"] == "", "Prefix"] = df["Filename"].apply(lambda x: str(x)[:4] if isinstance(x, str) else "")

# Overwrite cleaned file
df.to_csv(patch_file_path, index=False)

# === 4. Notion formatting functions ===
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").isoformat()
    except Exception:
        return datetime.now().isoformat()

def add_to_notion(entry):
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Filename": {"title": [{"text": {"content": entry["Filename"]}}]},
            "Phase": {"number": int(entry["Phase"])},
            "Module": {"rich_text": [{"text": {"content": entry["Module"]}}]},
            "Prefix": {"rich_text": [{"text": {"content": entry["Prefix"]}}]},
            "Status": {"select": {"name": entry["Status"]}},
            "Path": {"rich_text": [{"text": {"content": entry["Path"]}}]},
            "Last Updated": {"date": {"start": format_date(entry["Last Updated"])}}
        }
    )

# === 5. Upload each row to Notion ===
with open(patch_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            add_to_notion(row)
            print(f"✅ Added: {row['Filename']}")
        except Exception as e:
            print(f"❌ Failed to add: {row.get('Filename', 'Unknown')} → {e}")
