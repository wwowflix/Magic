import os, json, re, time
from pathlib import Path

ROOT = Path(os.environ.get("MAGIC_ROOT", ".")).resolve()
RRDIR = ROOT / "outputs" / "retry_requests"
OUTDIR = ROOT / "outputs" / "remediation"
MANIFEST = ROOT / "phase_manifest.json"

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def norm(name: str) -> str:
    import os, re
    b = os.path.basename(name or "")
    b = re.sub(r"\.py$", "", b, flags=re.I)
    b = re.sub(r"_(READY|DRAFT|HOLD)$", "", b, flags=re.I)
    return b.lower()

def load_latest_retry_request():
    if not RRDIR.exists():
        return None, []
    latest = None
    for p in sorted(RRDIR.glob("cleanup_retry_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        latest = p
        break
    if not latest:
        return None, []
    try:
        obj = json.loads(latest.read_text(encoding="utf-8") or "{}")
        return latest, obj.get("basenames", []) or []
    except Exception:
        return latest, []

def load_manifest():
    if not MANIFEST.exists():
        return []
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8") or "[]")
    except Exception:
        return []

def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    latest_file, basenames = load_latest_retry_request()
    mf = load_manifest()

    failed_norm = {norm(n) for n in basenames}
    matched = []
    for row in mf:
        fn = row.get("final_filename") or row.get("filename") or ""
        if fn and norm(fn) in failed_norm:
            matched.append(row)

    # write artifacts
    (OUTDIR / "manifest_retry_week11.json").write_text(json.dumps(matched, ensure_ascii=False, indent=2), encoding="utf-8")

    ranked = []
    for r in matched:
        ranked.append({
            "final_filename": r.get("final_filename") or r.get("filename"),
            "phase": r.get("phase"),
            "module": r.get("module"),
            "last_ts": now(),
            "count": 1
        })
    (OUTDIR / "prioritized_failures.json").write_text(json.dumps(ranked, ensure_ascii=False, indent=2), encoding="utf-8")

    runrec = {
        "ts": now(),
        "retry_request": str(latest_file) if latest_file else None,
        "requested": len(basenames),
        "matched": len(matched),
        "out_manifest": str(OUTDIR / "manifest_retry_week11.json"),
        "out_prioritized": str(OUTDIR / "prioritized_failures.json")
    }
    (OUTDIR / "orchestrator_run.json").write_text(json.dumps(runrec, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(runrec))
if __name__ == "__main__":
    main()
