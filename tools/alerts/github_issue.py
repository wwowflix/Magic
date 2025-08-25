import os, json
try:
    import requests  # type: ignore
except Exception:
    requests = None

def create_issue(title: str, body: str, labels=None):
    token = os.getenv("GH_TOKEN"); repo = os.getenv("GH_REPO")
    dry = (not token) or (not repo) or (requests is None)
    payload = {"title": title, "body": body}
    if labels: payload["labels"] = labels
    if dry:
        return {"channel":"github","dry_run":True,"id":None,"url":None,"repo":repo,"payload":payload}
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept":"application/vnd.github+json", "User-Agent":"MAGIC-bot"}
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    d = r.json()
    return {"channel":"github","dry_run":False,"id":d.get("number"),"url":d.get("html_url")}
if __name__=="__main__":
    import sys
    title = sys.argv[1] if len(sys.argv)>1 else "MAGIC: Failure detected"
    body  = sys.argv[2] if len(sys.argv)>2 else "See logs for details."
    print(json.dumps(create_issue(title, body)))
