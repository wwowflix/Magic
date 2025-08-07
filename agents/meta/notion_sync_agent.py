import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ================================
# 1️⃣ Load Environment Variables
# ================================
load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

SUMMARY_DIR = os.path.join('outputs', 'summaries')
NOTION_PAGE_SIZE = 100

# ================================
# 2️⃣ Session with Retry Logic
# ================================
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST", "PATCH"]
)
session.mount('https://', HTTPAdapter(max_retries=retries))


# ================================
# 3️⃣ Helpers
# ================================
def fetch_database_schema():
    """Fetch database schema to validate select options."""
    try:
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"
        resp = session.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get('properties', {})
    except Exception as e:
        print(f"⚠️ Failed to fetch schema: {e}")
        return {}


def query_database(start_cursor=None):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {"page_size": NOTION_PAGE_SIZE}
    if start_cursor:
        payload["start_cursor"] = start_cursor
    resp = session.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()


def get_all_pages():
    """Fetch all pages in the database."""
    pages = []
    cursor = None
    while True:
        data = query_database(cursor)
        pages.extend(data.get('results', []))
        if not data.get('has_more'):
            break
        cursor = data.get('next_cursor')
    return pages


def normalize_status(status, valid_statuses):
    """Ensure status matches valid options, else fallback."""
    if status in valid_statuses:
        return status
    fallback = valid_statuses[0] if valid_statuses else "Unknown"
    print(f"⚠️ Status '{status}' not valid, using '{fallback}'")
    return fallback


def create_page(script_name, phase, module, status, valid_statuses):
    """Create a new Notion page entry."""
    url = "https://api.notion.com/v1/pages"
    now = datetime.now(timezone.utc).isoformat()
    clean_status = normalize_status(status, valid_statuses)
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Script": {"title": [{"text": {"content": script_name}}]},
            "Phase": {"number": int(phase)},
            "Module": {"rich_text": [{"text": {"content": module}}]},
            "Status": {"select": {"name": clean_status}},
            "Last Updated": {"date": {"start": now}}
        }
    }
    try:
        print(f"➕ Creating: {script_name}")
        resp = session.post(url, headers=HEADERS, json=data)
        resp.raise_for_status()
    except requests.HTTPError as e:
        err = e.response.text if e.response is not None else str(e)
        print(f"⚠️ Error creating page for {script_name}: {err}")


def update_page(page_id, phase, module, status, valid_statuses):
    """Update an existing Notion page entry."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    now = datetime.now(timezone.utc).isoformat()
    clean_status = normalize_status(status, valid_statuses)
    data = {"properties": {
        "Phase": {"number": int(phase)},
        "Module": {"rich_text": [{"text": {"content": module}}]},
        "Status": {"select": {"name": clean_status}},
        "Last Updated": {"date": {"start": now}}
    }}
    try:
        print(f"✏️ Updating: {page_id}")
        resp = session.patch(url, headers=HEADERS, json=data)
        resp.raise_for_status()
    except requests.HTTPError as e:
        err = e.response.text if e.response is not None else str(e)
        print(f"⚠️ Error updating page {page_id}: {err}")


def read_latest_summary_files():
    """Return latest version of each summary file based on timestamp."""
    if not os.path.isdir(SUMMARY_DIR):
        print(f"⚠️ Summary directory not found: {SUMMARY_DIR}, skipping sync.")
        return []
    files = [f for f in os.listdir(SUMMARY_DIR) if f.endswith('_summary.tsv')]
    latest = {}
    for f in files:
        key = f.rsplit('_summary.tsv', 1)[0]
        path = os.path.join(SUMMARY_DIR, f)
        mtime = os.path.getmtime(path)
        if key not in latest or mtime > latest[key][1]:
            latest[key] = (path, mtime)
    return [v[0] for v in latest.values()]


# ================================
# 4️⃣ Main Sync Function
# ================================
def sync_to_notion():
    schema = fetch_database_schema()
    status_prop = schema.get('Status', {}).get('select', {}).get('options', [])
    valid_statuses = [opt['name'] for opt in status_prop] if status_prop else ["Unknown"]

    # Build lookup of existing pages
    pages = get_all_pages()
    existing_pages = {}
    for p in pages:
        title = p.get('properties', {}).get('Script', {}).get('title', [])
        if title:
            name = title[0].get('plain_text')
            if name:
                existing_pages[name] = p['id']

    summary_files = read_latest_summary_files()
    if not summary_files:
        print("⚠️ No summary files to process.")
        return

    for summary in summary_files:
        name = os.path.basename(summary)
        if not name.startswith('phase') or '_module_' not in name:
            print(f"⚠️ Skipping invalid file: {name}")
            continue
        phase_part, module_part = name.split('_module_')
        phase_num = phase_part.replace('phase', '')
        if not phase_num.isdigit():
            print(f"⚠️ Skipping non-numeric phase file: {name}")
            continue
        module = module_part.replace('_summary.tsv', '')

        with open(summary, encoding='utf-8') as f:
            _ = next(f, None)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) != 2:
                    print(f"⚠️ Skipping invalid line in {name}: {line.strip()}")
                    continue
                script_name, status = parts
                try:
                    if script_name in existing_pages:
                        update_page(existing_pages[script_name], phase_num, module, status, valid_statuses)
                    else:
                        create_page(script_name, phase_num, module, status, valid_statuses)
                except Exception as e:
                    print(f"⚠️ Error syncing {script_name}: {e}")

    print("✅ Notion sync complete.")


# ================================
# 5️⃣ Entry Point
# ================================
if __name__ == '__main__':
    sync_to_notion()
