"""
Notion Sync Agent – Updates the MAGIC Automation Tracker with latest file metadata
"""

import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
PATCH_FILE = "magic_patch.csv"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def update_notion_row(row):
    from datetime import datetime

    page_id = row["NotionPageID"]
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    props = {
        "Status": {"select": {"name": row["Status"]}},
        "Folder Location": {"rich_text": [{"text": {"content": row["Folder Location"]}}]},
        "Last Moved": {"date": {"start": datetime.now().isoformat()}},
    }

    data = {"properties": props}
    requests.patch(update_url, headers=headers, json=data)


def main():
    if not os.path.exists(PATCH_FILE):
        print(f"❌ Patch file not found: {PATCH_FILE}")
        return

    with open(PATCH_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("NotionPageID") and row.get("Status"):
                try:
                    update_notion_row(row)
                    print(f"✅ Synced: {row['Filename']}")
                except Exception as e:
                    print(f"❌ Failed: {row['Filename']} → {e}")


if __name__ == "__main__":
    main()
