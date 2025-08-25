import json, os, time
from pathlib import Path
from ai_remediator import apply_remediation_ai
from patcher import write_diff

ROOT = Path(os.environ.get("MAGIC_ROOT",".")\).resolve()
OUT = ROOT / "outputs" / "remediation"
ORCH_MANIFEST = OUT / "manifest_retry_week11.json"
PRIO = OUT / "prioritized_failures.json"
METRICS = OUT / "remediate_metrics.json"

def _now(): 
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _load_list():
    # Prefer orchestrator manifest, then prioritized list
    items = []
    if ORCH_MANIFEST.exists():
        try:
            items = json.loads(ORCH_MANIFEST.read_text(encoding="utf-8") or "[]")
        except: 
            items = []
    if not items and PRIO.exists():
        try:
            items = json.loads(PRIO.read_text(encoding="utf-8") or "[]")
        except:
            items = []
    # Normalize to filenames; search in repo if needed
    targets = []
    for x in items:
        fn = x.get("final_filename") or x.get("filename") or ""
        if fn:
            targets.append(fn)
    return targets

def _find_file(basename: str):
    # search common script roots
    roots = [ROOT / "scripts", ROOT / "phase11", ROOT]
    for r in roots:
        for p in r.rglob(basename):
            if p.is_file():
                return p
    # last resort: search by stem
    stem = Path(basename).stem
    for r in roots:
        for p in r.rglob(f"{stem}.py"):
            if p.is_file():
                return p
    return None

def append_metric(attempted: int, applied: int):
    try:
        arr = json.loads(METRICS.read_text(encoding="utf-8") or "[]")
        if not isinstance(arr, list): arr=[]
    except:
        arr = []
    arr.append({"attempted": attempted, "applied": applied, "ts": _now(), "source":"ai"})
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

def main(limit=5):
    basenames = _load_list()
    attempted = 0
    applied = 0
    for b in basenames[:limit]:
        path = _find_file(b)
        if not path:
            continue
        attempted += 1
        # In a real run, pass an error excerpt; here we omit or read neighboring log if desired
        sug = apply_remediation_ai(str(path), error_text="")
        diff_path, n = write_diff(str(path), sug["suggested_patch"])
        if n > 0:
            applied += 1
        print(f"[AI] {b} -> diff:{diff_path} ({n} chars) :: {sug['explanation']}")
    append_metric(attempted, applied)
    print(f"[AI] metrics: attempted={attempted}, applied={applied}")

if __name__ == "__main__":
    main()
