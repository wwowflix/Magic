import os, json, time
from pathlib import Path

ROOT = Path(os.environ.get("MAGIC_ROOT",".")).resolve()
OUT = ROOT / "outputs" / "remediation"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "alerts_sent.jsonl"
FAIL_JL = OUT / "fail_events.jsonl"  # one-per-line JSON failure events

def now(): 
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def read_latest_fail():
    if not FAIL_JL.exists(): return None
    try:
        lines = FAIL_JL.read_text(encoding="utf-8").splitlines()
        if not lines: return None
        return json.loads(lines[-1])
    except Exception:
        return None

def main(title=None, body=None):
    ev = read_latest_fail()
    if not title:
        title = (ev.get("title") if ev else "MAGIC: Failure detected")
    if not body:
        if ev:
            body = f"Module: {ev.get('module')}\nScript: {ev.get('script')}\nPhase: {ev.get('phase')}\nError: {ev.get('error','(see logs)')}\nTS: {ev.get('ts')}"
        else:
            body = "No event file; demo alert."

    # lazy import to avoid dependency issues
    from github_issue import create_issue
    from notion_page import create_page

    res_gh = create_issue(title, body, labels=["MAGIC","FAIL"])
    res_no = create_page(title, body)

    record = {
        "ts": now(),
        "title": title,
        "channels": [res_gh, res_no],
    }
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record))
if __name__=="__main__":
    import sys
    t = sys.argv[1] if len(sys.argv)>1 else None
    b = sys.argv[2] if len(sys.argv)>2 else None
    main(t,b)
