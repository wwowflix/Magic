import ast, pathlib, json, re, collections, csv

ROOT_SCRIPTS = pathlib.Path(r"D:/MAGIC/scripts")
OUT_JSON     = pathlib.Path(r"D:/MAGIC/outputs/reports/deps_graph.json")
OUT_TSV      = pathlib.Path(r"D:/MAGIC/outputs/reports/orphans_by_dir.tsv")
QUARANTINE   = pathlib.Path(r"D:/MAGIC/quarantine")  # ignore anything under quarantine

# Heuristics for "executables" that are OK to have zero inbound imports
WHITELIST_DIRS = [
    pathlib.Path(r"D:/MAGIC/scripts/phase11"),  # phase 11 pipelines/modules

    pathlib.Path(r"D:/MAGIC/scripts/phase02"),
    pathlib.Path(r"D:/MAGIC/scripts/phase03"),
    pathlib.Path(r"D:/MAGIC/scripts/phase04"),
    pathlib.Path(r"D:/MAGIC/scripts/phase05"),
    pathlib.Path(r"D:/MAGIC/scripts/phase13"),
    pathlib.Path(r"D:/MAGIC/scripts/phase14"),
    pathlib.Path(r"D:/MAGIC/scripts/phase18"),]
WHITELIST_REGEXES = [
    re.compile(r"_cli_READY\.py$", re.I),       # command-line entrypoints
    re.compile(r"runner", re.I),                # any runner keyword in filename
]
IGNORE_REGEXES = [
    re.compile(r"\\quarantine\\", re.I),        # quarantine
    re.compile(r"\\tests?\\", re.I),            # tests folders
    re.compile(r"_TEST_READY\.py$", re.I),      # test files
    re.compile(r"^__init___READY\.py$", re.I),  # init stubs
]

def is_ignored(p: pathlib.Path) -> bool:
    try:
        rp = p.resolve()
    except Exception:
        rp = p
    if QUARANTINE.exists() and QUARANTINE in rp.parents:
        return True
    s = str(p)
    return any(rx.search(s) for rx in IGNORE_REGEXES)

def is_whitelisted(p: pathlib.Path) -> bool:
    try:
        rp = p.resolve()
    except Exception:
        rp = p
    # directory-based
    for d in WHITELIST_DIRS:
        try:
            if hasattr(rp, "is_relative_to"):
                if rp.is_relative_to(d):
                    return True
            else:
                if str(rp).startswith(str(d)):
                    return True
        except Exception:
            pass
    # name patterns
    s = p.name
    if any(rx.search(s) for rx in WHITELIST_REGEXES):
        return True
    return False

def is_top_level_tool(p: pathlib.Path) -> bool:
    # exactly one level under scripts/ (standalone tools)
    try:
        return p.parent == ROOT_SCRIPTS
    except Exception:
        return False

def is_entrypoint(p: pathlib.Path) -> bool:
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
        return "__main__" in t
    except Exception:
        return False

def py_files():
    for p in ROOT_SCRIPTS.rglob("*_READY.py"):
        if is_ignored(p):
            continue
        yield p

def get_imports(p: pathlib.Path):
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(t)
    except Exception:
        return []
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add((a.name.split(".") or [""])[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                mods.add((n.module.split(".") or [""])[0])
    return sorted(mods)

def main():
    files = list(py_files())
    graph = {str(f).replace("\\\\","/"): get_imports(f) for f in files}

    stems = {k: pathlib.Path(k).stem for k in graph.keys()}
    inbound = {k: 0 for k in graph}
    for k, mods in graph.items():
        for m in mods:
            lm = m.lower()
            for path, stem in stems.items():
                if lm == stem.lower():
                    inbound[path] += 1

    orphans = []
    for k, v in inbound.items():
        p = pathlib.Path(k)
        if v == 0 and not (is_entrypoint(p) or is_whitelisted(p) or is_top_level_tool(p)):
            orphans.append(k)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"inbound": inbound, "orphans": orphans}, indent=2), encoding="utf-8")
    print(f"[11D] Wrote {OUT_JSON} (orphans: {len(orphans)})")

    # by-folder TSV to prioritize cleanup
    counts = collections.Counter(str(pathlib.Path(o).parent) for o in orphans)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["folder","orphans"])
        for folder, cnt in counts.most_common():
            w.writerow([folder, cnt])
    print(f"[11D] Wrote {OUT_TSV} (folders: {len(counts)})")

if __name__ == "__main__":
    main()

