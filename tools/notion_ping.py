import os, json, sys, urllib.request

root = r"E:\MAGIC"
env_path = os.path.join(root, ".env")
token = db = None

# read .env manually (no dotenv required)
with open(env_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("NOTION_TOKEN="):
            token = line.split("=",1)[1].strip()
        if line.startswith("NOTION_DATABASE_ID="):
            db = line.split("=",1)[1].strip()

if not token or not db:
    print("ERR|Missing NOTION_TOKEN or NOTION_DATABASE_ID")
    sys.exit(2)

url = f"https://api.notion.com/v1/databases/{db}"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Notion-Version", "2022-06-28")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.load(resp)
        title = "".join(t.get("plain_text","") for t in data.get("title", []))
        print("OK|" + (title or "Unnamed database"))
except Exception as e:
    print("ERR|" + repr(e))
    sys.exit(1)
