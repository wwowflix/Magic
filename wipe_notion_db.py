import os, requests, time

TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("NOTION_DATABASE_ID")
if not TOKEN or not DB_ID:
    raise RuntimeError("Make sure NOTION_TOKEN and NOTION_DATABASE_ID are set in your env")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# 1) Fetch all pages (with pagination)
all_pages = []
cursor = None
while True:
    payload = {"page_size": 100}
    if cursor:
        payload["start_cursor"] = cursor
    resp = requests.post(f"https://api.notion.com/v1/databases/{DB_ID}/query",
                         headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    all_pages.extend(data["results"])
    if not data.get("has_more"):
        break
    cursor = data["next_cursor"]
    time.sleep(0.3)  # gentle rate-limit

print(f"Found {len(all_pages)} pages to archive…")

# 2) Archive each one
for page in all_pages:
    page_id = page["id"]
    patch = {"archived": True}
    r = requests.patch(f"https://api.notion.com/v1/pages/{page_id}",
                       headers=headers, json=patch)
    if r.status_code == 200:
        print("✅ Archived", page_id)
    else:
        print("⚠️ Skipped", page_id, r.status_code, r.text)
    time.sleep(0.2)

print("🎉 Done. Database should now be empty!")
