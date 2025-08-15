import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
SUMMARY_FILE = "outputs/summaries/phase_master_summary.tsv"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def query_database_by_filename(filename):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Filename",
            "rich_text": {
                "equals": filename
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def update_status(page_id, new_status):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Status": {
                "select": {
                    "name": new_status
                }
            }
        }
    }
    requests.patch(url, json=payload, headers=headers)

def main():
    if not os.path.exists(SUMMARY_FILE):
        print(f"❌ Summary file not found: {SUMMARY_FILE}")
        return

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            filename = row["Script"]
            status = row["Status"]

            if status == "FAIL":
                print(f"🔄 Updating Notion for: {filename} → FAIL")
                result = query_database_by_filename(filename)
                results = result.get("results", [])
                if results:
                    page_id = results[0]["id"]
                    update_status(page_id, "❌ Failed")
                else:
                    print(f"⚠️ Notion page not found for: {filename}")

if __name__ == "__main__":
    main()
