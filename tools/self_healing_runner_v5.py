# -*- coding: utf-8 -*-
"""
Self-Healing Runner v5 — robust manifest reader + filters
Usage examples:
  python self_healing_runner_v5.py --manifest phase_manifest.json --list
  python self_healing_runner_v5.py --manifest phase_manifest.json --phases 11 --modules module_B --dry-run
  python self_healing_runner_v5.py --manifest phase_manifest.json --phases 11 --modules B
"""
import argparse, json, os, re, sys, subprocess
from typing import Any, Dict, List

def load_manifest(path: str) -> List[Dict[str, Any]]:
    text = open(path, 'r', encoding='utf-8-sig').read().strip()
    data = None
    try:
        data = json.loads(text)
    except Exception:
        # Try NDJSON (one JSON object per line)
        arr = []
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            try:
                arr.append(json.loads(s))
            except Exception:
                pass
        if arr:
            data = arr
    if data is None:
        raise SystemExit(f"Could not parse manifest: {path}")

    # Normalize to a list
    if isinstance(data, list):
        arr = data
    elif isinstance(data, dict):
        for key in ("entries", "manifest", "data", "items", "rows"):
            if isinstance(data.get(key), list):
                arr = data[key]
                break
        else:
            # Single object — wrap
            arr = [data]
    else:
        arr = [data]

    # Ensure all entries are dicts
    out = []
    for e in arr:
        if isinstance(e, dict):
            out.append(e)
    return out

def norm_module(s: Any) -> str:
    if s is None:
        return ""
    s = str(s)
    # normalize: "Module B", "module_B", "B" -> "module_b" or "b" variants acceptable
    s2 = s.lower().strip()
    s2 = s2.replace(" ", "_")
    return s2

def norm_phase(v: Any) -> int:
    if v is None or v == "":
        return -1
    try:
        return int(str(v).strip())
    except Exception:
        # Try to pull digits
        m = re.search(r"\d+", str(v))
        return int(m.group()) if m else -1

def coalesce(d: Dict[str, Any], *keys):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None

def choose_script_path(root: str, entry: Dict[str, Any]) -> str:
    # Prefer explicit path fields
    p = coalesce(entry, "Path", "FullPath", "ScriptPath", "path")
    if p:
        return os.path.normpath(os.path.join(root, p) if not os.path.isabs(p) else p)
    # Fall back to FinalFilename/Filename under conventional layout
    fn = coalesce(entry, "FinalFilename", "Filename", "file", "Script")
    phase = norm_phase(coalesce(entry, "Phase", "PhaseNumber", "phase"))
    mod   = norm_module(coalesce(entry, "Module", "ModuleName", "module"))
    if fn and phase >= 0 and mod:
        # try standard scripts/phase{n}/{module}/filename
        guess = os.path.join(root, "scripts", f"phase{phase}", mod, fn)
        return os.path.normpath(guess)
    # last resort: if there's only a filename, try to find it under scripts
    if fn:
        for base in ("scripts",):
            candidate = os.path.join(root, base, fn)
            if os.path.exists(candidate):
                return os.path.normpath(candidate)
    return ""

def entry_matches(entry: Dict[str, Any], phases: List[int], modules: List[str]) -> bool:
    ep = norm_phase(coalesce(entry, "Phase", "PhaseNumber", "phase"))
    em = norm_module(coalesce(entry, "Module", "ModuleName", "module"))
    # module may also be implied by path
    p  = coalesce(entry, "Path", "FullPath", "ScriptPath", "path") or ""
    pm = norm_module("module_" + re.sub(r".*\\(module_[a-z])\\.*", r"\1", p.lower()).replace("\\", "")) if "module_" in p.lower() else ""

    if phases and ep not in phases:
        return False

    if modules:
        # Accept: "b", "module_b", "module b"
        wanted = set()
        for m in modules:
            m2 = norm_module(m)
            wanted.add(m2)
            if re.fullmatch(r"[a-z]", m2):
                wanted.add(f"module_{m2}")
        if em in wanted or pm in wanted:
            return True
        return False
    return True

def run_scripts(entries: List[Dict[str, Any]], dry_run: bool) -> int:
    root = os.getcwd()
    ok = 0; fail = 0
    for e in entries:
        spath = choose_script_path(root, e)
        fn = coalesce(e, "FinalFilename", "Filename", "file", "Script") or os.path.basename(spath)
        phase = norm_phase(coalesce(e, "Phase", "PhaseNumber", "phase"))
        mod   = norm_module(coalesce(e, "Module", "ModuleName", "module")) or "unknown"

        if not spath:
            print(f"⚠️  Skip (no path): {fn}")
            fail += 1
            continue

        print(("DRY-RUN  " if dry_run else "") + f"▶ {spath}")
        if dry_run:
            continue

        os.makedirs(os.path.join("outputs","logs", f"phase{phase}_{mod}"), exist_ok=True)
        log_path = os.path.join("outputs","logs", f"phase{phase}_{mod}", f"{os.path.splitext(fn)[0]}.log")

        with open(log_path, "w", encoding="utf-8") as lf:
            proc = subprocess.run([sys.executable, spath], stdout=lf, stderr=lf)
            if proc.returncode == 0:
                print(f"✅ PASS {fn}")
                ok += 1
            else:
                print(f"❌ FAIL {fn} (exit {proc.returncode})  → {log_path}")
                fail += 1
    print(f"\nSummary: OK={ok}  FAIL={fail}  TOTAL={ok+fail}")
    return 0 if fail == 0 else 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest","-m", required=True)
    ap.add_argument("--phases", nargs="+", type=int, default=[])
    ap.add_argument("--modules", nargs="+", default=[])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true", help="List matching entries and exit")
    args = ap.parse_args()

    manifest = load_manifest(args.manifest)
    if not manifest:
        print("Manifest is empty.")
        sys.exit(1)

    entries = [e for e in manifest if isinstance(e, dict)]
    # If no filters, default to "everything"
    phases  = args.phases
    modules = args.modules

    # Filter
    filt = [e for e in entries if entry_matches(e, phases, modules)]

    # If filters produce nothing but no filters were passed, use all
    if not filt and not phases and not modules:
        filt = entries

    if not filt:
        print("No matching entries found in manifest. Nothing to run.")
        # Help: show some diagnostics
        sample = entries[:3]
        keys = sorted({k for e in sample for k in e.keys()})
        print(f"Hint: keys seen = {keys}")
        sys.exit(0)

    if args.list or args.dry_run:
        print(f"Matched {len(filt)} entr{'y' if len(filt)==1 else 'ies'}:")
        root = os.getcwd()
        for e in filt:
            phase = norm_phase(coalesce(e, "Phase","PhaseNumber","phase"))
            mod   = norm_module(coalesce(e, "Module","ModuleName","module"))
            fn    = coalesce(e, "FinalFilename","Filename","file","Script") or ""
            spath = choose_script_path(root, e)
            print(f"  - phase={phase} module={mod or '?'} file={fn or os.path.basename(spath)} path={spath}")
        if args.dry_run:
            sys.exit(0)

    sys.exit(run_scripts(filt, dry_run=False))

if __name__ == "__main__":
    main()
