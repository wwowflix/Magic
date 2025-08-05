import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

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

def query_database(start_cursor=None):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    data = {"page_size": NOTION_PAGE_SIZE}
    if start_cursor:
        data["start_cursor"] = start_cursor
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()

def get_all_pages():
    pages = []
    cursor = None
    while True:
        data = query_database(cursor)
        pages.extend(data['results'])
        if not data.get('has_more'):
            break
        cursor = data.get('next_cursor')
    return pages

def create_or_update_page(script_name, phase, module, status):
    # Search if page already exists
    pages = get_all_pages()
    for page in pages:
        props = page['properties']
        if props.get('Script') and props['Script']['title'][0]['plain_text'] == script_name:
            # Update existing page
            update_page(page['id'], phase, module, status)
            return
    # Create new page
    create_page(script_name, phase, module, status)

def create_page(script_name, phase, module, status):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Script": {
                "title": [
                    {"text": {"content": script_name}}
                ]
            },
            "Phase": {
                "rich_text": [
                    {"text": {"content": phase}}
                ]
            },
            "Module": {
                "rich_text": [
                    {"text": {"content": module}}
                ]
            },
            "Status": {
                "select": {"name": status}
            },
            "Last Updated": {
                "date": {"start": datetime.utcnow().isoformat()}
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()

def update_page(page_id, phase, module, status):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {
        "properties": {
            "Phase": {
                "rich_text": [
                    {"text": {"content": phase}}
                ]
            },
            "Module": {
                "rich_text": [
                    {"text": {"content": module}}
                ]
            },
            "Status": {
                "select": {"name": status}
            },
            "Last Updated": {
                "date": {"start": datetime.utcnow().isoformat()}
            }
        }
    }
    response = requests.patch(url, headers=HEADERS, json=data)
    response.raise_for_status()

def read_latest_summary_files():
    # Collect latest summary files in outputs/summaries
    files = [f for f in os.listdir(SUMMARY_DIR) if f.endswith('_summary.tsv')]
    latest_files = {}
    for f in files:
        # Use file's modification time as key to get latest for each phase_module
        phase_module = f.replace('_summary.tsv','')
        filepath = os.path.join(SUMMARY_DIR, f)
        mtime = os.path.getmtime(filepath)
        if phase_module not in latest_files or mtime > latest_files[phase_module][1]:
            latest_files[phase_module] = (filepath, mtime)
    return [v[0] for v in latest_files.values()]

def sync_to_notion():
    summary_files = read_latest_summary_files()
    for summary_file in summary_files:
        # Extract phase and module from filename
        basename = os.path.basename(summary_file)
        try:
            phase_module = basename.replace('_summary.tsv','')
            phase, module = phase_module.split('_module_')
        except Exception:
            continue
        with open(summary_file, 'r', encoding='utf-8') as f:
            next(f)  # skip header
            for line in f:
                script_name, status = line.strip().split('\t')
                create_or_update_page(script_name, phase, module, status)
    print(f"✅ Notion sync complete. Synced {len(summary_files)} summary files.")

if __name__ == "__main__":
    sync_to_notion()
