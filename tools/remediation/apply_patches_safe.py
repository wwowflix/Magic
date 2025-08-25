import os, json, time, re, shutil
from pathlib import Path

ROOT = Path(os.environ.get("MAGIC_ROOT",".")).resolve()
SUGDIR = ROOT / "outputs" / "remediation" / "ai_suggestions"
BACKUPS = ROOT / "outputs" / "remediation" / "backups" / time.strftime("%Y%m%d_%H%M%S")
METRICS = ROOT / "outputs" / "remediation" / "remediate_metrics.json"

def find_script(script_name:str):
    # search common roots
    roots = [ROOT/"scripts", ROOT/"phase11", ROOT]
    for r in roots:
        for p in r.rglob(script_name):
            if p.is_file(): return p
    # fallback by stem
    stem = Path(script_name).stem
    for r in roots:
        for p in r.rglob(f"{stem}.py"):
            if p.is_file(): return p
    return None

def latest_suggestion_for(file_stem: Path):
    f = SUGDIR / f"{file_stem}.jsonl"
    if not f.exists(): return None
    try:
        lines = f.read_text(encoding="utf-8").splitlines()
        if not lines: return None
        return json.loads(lines[-1])
    except: return None

def append_metric(attempted:int, applied:int, source="ai-apply"):
    try:
        arr = json.loads(METRICS.read_text(encoding="utf-8") or "[]")
        if not isinstance(arr, list): arr=[]
    except: arr=[]
    arr.append({"attempted": attempted, "applied": applied, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source": source})
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

def main(limit=5):
    if not SUGDIR.exists():
        print("no ai_suggestions dir")
        append_metric(0,0); return
    suggestions = sorted(SUGDIR.glob("*.jsonl"))
    attempted=0; applied=0
    BACKUPS.mkdir(parents=True, exist_ok=True)
    for log in suggestions[:limit]:
        stem = log.stem  # script stem
        sug = latest_suggestion_for(stem)
        if not sug: continue
        target = find_script(sug.get("script", stem+".py"))
        if not target: continue
        new_text = sug.get("suggested_patch","")
        if not new_text: continue
        attempted += 1
        # backup
        rel = target.name
        bpath = BACKUPS / rel
        try:
            shutil.copy2(str(target), str(bpath))
        except Exception:
            pass
        # apply
        try:
            target.write_text(new_text, encoding="utf-8")
            applied += 1
        except Exception:
            # restore on failure
            if bpath.exists():
                shutil.copy2(str(bpath), str(target))
    append_metric(attempted, applied)
    print(f"applied {applied}/{attempted} patches; backups at {BACKUPS}")
if __name__=="__main__":
    main()
