import os
import re
import requests
import datetime
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv(dotenv_path="D:/MAGIC/.env")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
MAGIC_ROOT = r"D:\MAGIC\scripts"

# ✅ Validate environment variables
if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ ERROR: Please set NOTION_TOKEN and NOTION_DATABASE_ID in your .env file.")
    exit(1)

# ✅ Notion API Headers
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 🔎 Extract phase/module metadata from filename
def extract_metadata(filename: str):
    match = re.match(r"(\d{2})([A-Z])_.*_READY\.py", filename)
    if match:
        phase = int(match.group(1))
        module = match.group(2)
        prefix = f"{phase:02}{module}_"
        return {
            "Phase": phase,
            "Module": module,
            "Prefix": prefix,
            "Status": "Ready"
        }
    return None

# 📂 Find *_READY.py scripts that are NOT placeholders
def find_ready_scripts():
    file_data = []
    for root, _, files in os.walk(MAGIC_ROOT):
        for file in files:
            if file.endswith("_READY.py"):
                full_path = os.path.join(root, file)

                # ✅ Skip placeholder files (those that start with '# Placeholder')
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        contents = f.read().strip()
                        if contents.lower().startswith("# placeholder"):
                            print(f"⚠️ Skipped placeholder: {file}")
                            continue
                except Exception as e:
                    print(f"❌ Could not read file {file}: {e}")
                    continue

                metadata = extract_metadata(file)
                if metadata:
                    metadata["Filename"] = file
                    metadata["Path"] = full_path
                    metadata["Last Updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                    file_data.append(metadata)
    return file_data

# 🔍 Search Notion for existing entry
def notion_search(filename):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Filename",
            "title": {
                "equals": filename
            }
        }
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        results = response.json().get("results", [])
        if results:
            return results[0]["id"]
    except Exception as e:
        print(f"❌ Error during search for {filename}: {e}")
    return None

# 🆕 Create new Notion row
def create_notion_page(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": format_notion_props(data)
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        return response.ok
    except Exception as e:
        print(f"❌ Failed to create: {data['Filename']} → {e}")
        return False

# 🔁 Update existing Notion row
def update_notion_page(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": format_notion_props(data)
    }
    try:
        response = requests.patch(url, headers=HEADERS, json=payload)
        return response.ok
    except Exception as e:
        print(f"❌ Failed to update: {data['Filename']} → {e}")
        return False

# 🧱 Format properties for Notion API
def format_notion_props(data):
    return {
        "Filename": {"title": [{"text": {"content": data["Filename"]}}]},
        "Phase": {"number": data["Phase"]},
        "Module": {"rich_text": [{"text": {"content": data["Module"]}}]},
        "Prefix": {"rich_text": [{"text": {"content": data["Prefix"]}}]},
        "Status": {"select": {"name": data["Status"]}},
        "Path": {"rich_text": [{"text": {"content": data["Path"]}}]},
        "Last Updated": {"date": {"start": data["Last Updated"]}}
    }

# 🚀 Main sync logic
def sync_to_notion():
    scripts = find_ready_scripts()
    print(f"🔍 Found {len(scripts)} real READY scripts...")

    for script in scripts:
        page_id = notion_search(script["Filename"])
        if page_id:
            updated = update_notion_page(page_id, script)
            print(f"🔁 Updated: {script['Filename']}" if updated else f"❌ Failed to update: {script['Filename']}")
        else:
            created = create_notion_page(script)
            print(f"🆕 Created: {script['Filename']}" if created else f"❌ Failed to create: {script['Filename']}")

# 🧪 CLI test option
if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        print("✅ Test OK: Environment variables loaded successfully.")
    else:
        sync_to_notion()
