import csv
import os
from notion_client import Client
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Check for valid token and DB
if not NOTION_TOKEN or not NOTION_DATABASE_ID:
    print("❌ NOTION_TOKEN or NOTION_DATABASE_ID missing from .env")
    exit(1)

notion = Client(auth=NOTION_TOKEN)

# Path to patch CSV
patch_file_path = "outputs/notion_export/magic_patch.csv"


def create_notion_entry(row):
    try:
        filename = row.get("Filename", "").strip()
        prefix = row.get("Prefix", "").strip()
        phase = int(row.get("Phase", 0))
        module = row.get("Module", "").strip()
        status = row.get("Status", "Pending").strip()
        is_placeholder = row.get("Is Placeholder", "False").strip().lower() == "true"
        is_implemented = row.get("Is Implemented", "False").strip().lower() == "true"
        folder_location = row.get("Folder Location", "").strip()
        notes = row.get("Notes", "").strip()
        last_synced = row.get("Last Synced", "").strip()

        # Build Notion page
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Filename": {"title": [{"text": {"content": filename}}]},
                "Prefix": {"rich_text": [{"text": {"content": prefix}}]},
                "Phase": {"number": phase},
                "Module": {"select": {"name": module}},
                "Status": {"select": {"name": status}},
                "Is Placeholder": {"checkbox": is_placeholder},
                "Is Implemented": {"checkbox": is_implemented},
                "Folder Location": {"rich_text": [{"text": {"content": folder_location}}]},
                "Notes": {"rich_text": [{"text": {"content": notes}}]} if notes else {},
                "Last Synced": (
                    {"rich_text": [{"text": {"content": last_synced}}]} if last_synced else {}
                ),
            },
        )
        print(f"✅ Added: {filename}")

    except Exception as e:
        print(f"❌ Failed to add: {filename} → {e}")


# Main Execution
if __name__ == "__main__":
    if not os.path.exists(patch_file_path):
        print(f"❌ File not found: {patch_file_path}")
        exit(1)

    with open(patch_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("Filename") and row.get("Prefix"):
                create_notion_entry(row)
            else:
                print(f"⚠️ Skipped row (missing Filename or Prefix): {row}")
