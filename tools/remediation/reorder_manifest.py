import argparse, json, re, os, time
from pathlib import Path

def norm(name:str)->str:
    if not name: return ""
    base = Path(name).name
    base = re.sub(r"\.py$","",base,flags=re.I)
    base = re.sub(r"_(READY|DRAFT|HOLD)$","",base,flags=re.I)
    return base.lower()

def load_json(p, default="[]"):
    try:
        t = Path(p).read_text(encoding="utf-8")
        return json.loads(t or default)
    except:
        return json.loads(default)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="phase_manifest.json")
    ap.add_argument("--priority", default="outputs/remediation/prioritized_failures.json")
    ap.add_argument("--out", default="outputs/remediation/ordered_manifest.json")
    args = ap.parse_args()

    mf = load_json(args.manifest)
    pr = load_json(args.priority)
    order = {}
    for i,x in enumerate(pr):
        fn = x.get("final_filename") or x.get("filename") or ""
        order[norm(fn)] = i

    def key(row):
        fn = row.get("final_filename") or row.get("filename") or ""
        n  = norm(fn)
        inprio = 0 if n in order else 1
        pri_ix = order.get(n, 1_000_000)
        # prefer lower (phase string '11A' -> phase number 11)
        phase_raw = str(row.get("phase",""))
        m = re.match(r"(\d+)", phase_raw)
        phase_num = int(m.group(1)) if m else 999
        return (inprio, pri_ix, phase_num, n)

    ordered = sorted(mf, key=key)
    outp = Path(args.out); outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(ordered, ensure_ascii=False, indent=2), encoding="utf-8")

    Path(outp.parent/"ordering_run.json").write_text(
        json.dumps({"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "manifest":str(Path(args.manifest).resolve()),
                    "priority":str(Path(args.priority).resolve()),
                    "out":str(outp.resolve()),
                    "prioritized_count":len(pr)}, indent=2),
        encoding="utf-8"
    )
    print(f"ordered -> {outp}")
if __name__=="__main__":
    main()
