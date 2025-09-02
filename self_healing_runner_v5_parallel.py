# -*- coding: utf-8 -*-
import argparse, json, os, re, sys, subprocess, concurrent.futures, datetime
from typing import Any, Dict, List, Optional, Tuple

# ---------- manifest loading ----------

def _json_loads(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None

def read_manifest(path: str) -> List[Dict[str, Any]]:
    """Return a list of dict entries, no matter if manifest is JSON array, JSONL, or dict-wrapped."""
    try:
        raw = open(path, "r", encoding="utf-8-sig").read()
    except FileNotFoundError:
        print(f"Manifest not found: {path}")
        return []

    data = _json_loads(raw)

    # Case 1: proper JSON array
    if isinstance(data, list):
        items = data
    # Case 2: dict-wrapped (try to find a list inside)
    elif isinstance(data, dict):
        items = None
        for v in data.values():
            if isinstance(v, list) and v:
                items = v
                break
        items = items or []
    else:
        # Case 3: JSONL fallback
        items = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            obj = _json_loads(line)
            if obj is not None:
                items.append(obj)

    # Normalize: try to turn stringified JSON rows into dicts
    norm: List[Dict[str, Any]] = []
    for it in items:
        if isinstance(it, dict):
            norm.append(it)
        elif isinstance(it, str):
            obj = _json_loads(it)
            if isinstance(obj, dict):
                norm.append(obj)
    return norm

# ---------- helpers & normalization ----------

def pick(d: Dict[str, Any], *keys) -> Optional[Any]:
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None

_digit_re = re.compile(r"\d+")

def normalize_phase(entry: Dict[str, Any]) -> Optional[int]:
    v = pick(entry, "Phase", "PhaseNumber", "phase")
    if v is not None:
        s = str(v).strip()
        try:
            return int(s)
        except Exception:
            m = _digit_re.search(s)
            if m:
                try:
                    return int(m.group(0))
                except Exception:
                    pass
    p = pick(entry, "Path", "FullPath", "ScriptPath")
    if p:
        m = re.search(r"[\\/]phase(\d+)[\\/]", p, flags=re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
    fn = pick(entry, "FinalFilename", "Filename", "file", "Script")
    if fn:
        m = re.match(r"(\d+)[A-Za-z]\_", fn)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
    return None

def module_letter(s: str) -> Optional[str]:
    if not s:
        return None
    t = s.strip().lower()
    m = re.search(r"module[\s_]*([a-z0-9]+)$", t)
    if m:
        return m.group(1).upper()
    m = re.fullmatch(r"([a-z0-9])", t)
    if m:
        return m.group(1).upper()
    m = re.search(r"\bmodule\s+([a-z0-9]+)$", t)
    if m:
        return m.group(1).upper()
    return None

def normalize_module(entry: Dict[str, Any]) -> Optional[str]:
    v = pick(entry, "Module", "ModuleName", "module")
    if v:
        ml = module_letter(str(v))
        if ml:
            return ml
    p = pick(entry, "Path", "FullPath", "ScriptPath")
    if p:
        m = re.search(r"[\\/](module[_\s]*([a-z0-9]+))[\\/]", p, flags=re.IGNORECASE)
        if m:
            return m.group(2).upper()
    fn = pick(entry, "FinalFilename", "Filename", "file", "Script")
    if fn:
        m = re.match(r"\d+([A-Za-z0-9])\_", fn)
        if m:
            return m.group(1).upper()
    return None

def build_path(entry: Dict[str, Any], ph: Optional[int], modL: Optional[str]) -> Optional[str]:
    p = pick(entry, "Path", "FullPath", "ScriptPath")
    if p:
        return p
    fn = pick(entry, "FinalFilename", "Filename", "file", "Script")
    if ph is not None and modL and fn:
        mod_dir = f"module_{modL.upper()}"
        return os.path.join("scripts", f"phase{ph}", mod_dir, fn)
    return None

# ---------- filtering & execution ----------

def parse_modules_cli(mods: Optional[List[str]]) -> Optional[set]:
    if not mods:
        return None
    out = set()
    for m in mods:
        token = module_letter(m) or m.strip().upper()
        out.add(token)
    return out

def collect_entries(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for e in data:
        if not isinstance(e, dict):
            continue
        ph = normalize_phase(e)
        mod = normalize_module(e)
        path = build_path(e, ph, mod)
        if ph is None or mod is None or not path:
            continue
        out.append({"phase": ph, "module": mod, "path": path})
    return out

def filter_entries(entries: List[Dict[str, Any]], phases: Optional[List[int]], modules: Optional[List[str]]) -> List[Dict[str, Any]]:
    pset = set(int(p) for p in phases) if phases else None
    mset = parse_modules_cli(modules)
    out = []
    for it in entries:
        if pset and it["phase"] not in pset:
            continue
        if mset and it["module"] not in mset:
            continue
        out.append(it)
    return out

def run_one(task):
    """Run a single script and capture output safely in UTF-8."""
    import os, sys, subprocess
    path = task["path"]
    env = os.environ.copy()
    # Force UTF-8 so weird bytes don't crash the reader threads on Windows
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        res = subprocess.run(
            [sys.executable, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",   # never crash on undecodable bytes
            env=env,
        )
        ok = (res.returncode == 0)
        return ok, path, res.stdout, res.stderr
    except FileNotFoundError:
        return False, path, "", "FileNotFoundError"
    except Exception as ex:
        return False, path, "", f"EXCEPTION: {ex}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m","--manifest", required=True)
    ap.add_argument("--phases", nargs="+", type=int)
    ap.add_argument("--modules", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--list", action="store_true", help="List matched scripts and exit")
    ap.add_argument("--limit", type=int, default=25, help="Limit listing output")
    args = ap.parse_args()

    data = read_manifest(args.manifest)
    all_entries = collect_entries(data)
    matches = filter_entries(all_entries, args.phases, args.modules)

    if not matches:
        print("No matching entries found in manifest. Nothing to run.")
        print("Hints: verify manifest has Phase/Module or path like scripts\\phase11\\module_C\\*.py")
        print("       try: --modules C   (not module_C), or omit --modules and only use --phases 11")
        return

    if args.list or args.dry_run:
        print(f"🔹 Matches: {len(matches)}")
        for it in matches[: max(1, args.limit)]:
            print(f"[P{it['phase']} M{it['module']}] {it['path']}")
        if len(matches) > args.limit:
            print(f"... and {len(matches)-args.limit} more")
        if args.dry_run or args.list:
            return

    ok = fail = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=max(1, args.parallel)) as ex:
        for res_ok, path, _out, _err in ex.map(run_one, matches):
            print(("OK   " if res_ok else "FAIL ") + path)
            if res_ok: ok += 1
            else: fail += 1

    total = ok + fail
    line = f"Summary: OK={ok}  FAIL={fail}  TOTAL={total}"
    print(line)
    os.makedirs(os.path.join("outputs","logs"), exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join("outputs","logs", f"runner_summary_{stamp}.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")

if __name__ == "__main__":
    main()
