import os
from notion_client import Client
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

if not NOTION_TOKEN or not NOTION_DATABASE_ID:
    raise ValueError(
        "❌ Please set NOTION_TOKEN and NOTION_DATABASE_ID in your .env file."
    )

notion = Client(auth=NOTION_TOKEN)


def fetch_database_rows():
    print("🔍 Fetching entries from Notion...")
    results = []
    next_cursor = None

    while True:
        response = notion.databases.query(
            database_id=NOTION_DATABASE_ID, start_cursor=next_cursor, page_size=100
        )
        results.extend(response["results"])
        next_cursor = response.get("next_cursor")
        if not next_cursor:
            break
    return results


def delete_duplicates(rows):
    filename_map = defaultdict(list)

    for row in rows:
        props = row.get("properties", {})
        title_obj = props.get("Filename", {}).get("title", [])

        # Safely skip if title is missing or malformed
        if not title_obj or "text" not in title_obj[0]:
            continue

        filename = title_obj[0]["text"].get("content", None)
        if not filename:
            continue

        filename_map[filename].append(row["id"])

    duplicates = {k: v for k, v in filename_map.items() if len(v) > 1}

    if not duplicates:
        print("✅ No duplicates found!")
        return

    print(f"⚠️ Found {len(duplicates)} duplicate filenames. Deleting extras...")

    for filename, ids in duplicates.items():
        # Keep the first and delete the rest
        for page_id in ids[1:]:
            notion.pages.update(page_id=page_id, archived=True)
            print(f"🗑️ Archived duplicate: {filename} → {page_id}")


if __name__ == "__main__":
    rows = fetch_database_rows()
    delete_duplicates(rows)
