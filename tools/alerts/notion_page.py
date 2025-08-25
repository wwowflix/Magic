import os, json
try:
    import requests  # type: ignore
except Exception:
    requests = None

NOTION_VERSION = os.getenv("NOTION_VERSION","2022-06-28")

def create_page(title: str, body: str):
    token = os.getenv("NOTION_TOKEN"); dbid = os.getenv("NOTION_DATABASE_ID")
    dry = (not token) or (not dbid) or (requests is None)
    payload = {
        "parent": {"database_id": dbid if dbid else "missing"},
        "properties": {
            "Name": {"title":[{"text":{"content": title[:200]}}]}
        },
        "children": [
            {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content": body[:1900]}}]}}
        ]
    }
    if dry:
        return {"channel":"notion","dry_run":True,"id":None,"url":None,"payload":payload}
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "User-Agent":"MAGIC-bot"
    }
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    d = r.json()
    return {"channel":"notion","dry_run":False,"id":d.get("id"),"url":d.get("url")}
if __name__=="__main__":
    import sys
    title = sys.argv[1] if len(sys.argv)>1 else "MAGIC: Failure detected"
    body  = sys.argv[2] if len(sys.argv)>2 else "See logs for details."
    print(json.dumps(create_page(title, body)))
