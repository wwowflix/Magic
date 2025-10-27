import os, sys, json, re, ast, fnmatch, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SRC_DIRS = [ROOT / "scripts", ROOT / "tools"]
OUT_DIR = ROOT / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COVER_XML = OUT_DIR / "coverage.xml"  # result of pytest --cov
MAX_SIZE_BYTES = 1_500_000  # skip > ~1.5 MB (tune if needed)

# Pull omit patterns from a local list; matches your .coveragerc
OMIT_PATTERNS = [
    "*/tests/*","*/venv/*","*/site-packages/*","*/__pycache__/*",
    "*/build/*","*/dist/*","*/.git/*","outputs/*","logs/*","backups/*",
    "scripts/*_READY.py","scripts/*_WIP.py","scripts/*_DRAFT.py",
    "scripts/reddit_api_*.py","scripts/cost_guard_2.py","scripts/lexer.py",
    "scripts/line_break.py","scripts/python_parser.py","scripts/test_encoding.py",
    "scripts/utils_*.py",
]

def is_omitted(p: Path) -> bool:
    s = str(p.as_posix())
    for pat in OMIT_PATTERNS:
        if fnmatch.fnmatch(s, pat):
            return True
    return False

def load_coverage():
    cov = {}
    if not COVER_XML.exists():
        return cov
    try:
        tree = ET.parse(str(COVER_XML))
        root = tree.getroot()
        for cls in root.findall(".//class"):
            fname = (cls.attrib.get("filename") or "").replace("\\","/")
            lines = cls.find("lines")
            hits = total = 0
            if lines is not None:
                for ln in lines.findall("line"):
                    total += 1
                    if int(ln.attrib.get("hits","0")) > 0:
                        hits += 1
            cov[fname] = {"covered": hits, "total": total,
                          "pct": (hits/total*100.0) if total else None}
    except Exception:
        pass
    return cov

def file_cov_for(path: Path, cov_map):
    if not cov_map: return None
    rel = str(path.relative_to(ROOT).as_posix())
    for key in (rel, rel.lstrip("./")):
        if key in cov_map: return cov_map[key]
    # last resort: endswith match
    for key in cov_map:
        if key.endswith(rel): return cov_map[key]
    return None

def classify_text(text: str) -> str:
    stripped = [ln.strip() for ln in text.splitlines()]
    nonblank = [ln for ln in stripped if ln]
    if not nonblank:
        return "empty"
    blob = "\n".join(nonblank).lower()
    if "raise notimplementederror" in blob:
        return "placeholder"
    only_defs = all(
        ln.startswith(("def ","class ","#")) or ln=="pass"
        for ln in nonblank
    )
    if len(nonblank) <= 8 and only_defs:
        return "placeholder"
    return "real"

def parse_ok(path: Path):
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
        ast.parse(src, filename=str(path))
        return True, "", src
    except Exception as e:
        try:
            src = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            src = ""
        return False, f"{e.__class__.__name__}: {e}", src

def scan():
    cov_map = load_coverage()
    rows = []
    totals = {"files":0,"real":0,"placeholder":0,"empty":0,"broken":0,
              "covered_lines":0,"total_lines":0}

    for base in SRC_DIRS:
        if not base.exists(): continue
        for p in base.rglob("*.py"):
            if any(part == "__pycache__" for part in p.parts): continue
            if is_omitted(p): continue
            if p.stat().st_size > MAX_SIZE_BYTES:  # skip massive files
                continue

            ok, err, src = parse_ok(p)
            status = "real" if ok else "broken"
            if ok:
                name = p.name
                if name.endswith(("_READY.py","_WIP.py","_DRAFT.py")):
                    status = "placeholder"
                else:
                    guess = classify_text(src)
                    if guess in ("placeholder","empty"):
                        status = guess

            cov = file_cov_for(p, cov_map) or {"covered":0,"total":0,"pct":None}
            rel = str(p.relative_to(ROOT)).replace("\\","/")
            rows.append({
                "path": rel,
                "status": status,
                "syntax_ok": ok,
                "cov_covered": cov["covered"],
                "cov_total": cov["total"],
                "cov_pct": None if cov["pct"] is None else round(cov["pct"],1),
                "lines": src.count("\n")+1 if src else 0,
                "size_bytes": p.stat().st_size,
                "syntax_error": err,
            })
            totals["files"] += 1
            totals[status] = totals.get(status,0)+1
            totals["covered_lines"] += cov["covered"]
            totals["total_lines"] += cov["total"]

    order = {"broken":0,"placeholder":1,"real":2,"empty":3}
    rows.sort(key=lambda r: (order.get(r["status"],9), r["path"]))

    summary = {
        "scanned_at": datetime.utcnow().isoformat()+"Z",
        "root": str(ROOT),
        "totals": totals,
        "coverage_overall_pct": round((totals["covered_lines"]/totals["total_lines"]*100.0),1)
                               if totals["total_lines"] else None
    }

    # TSV
    tsv = OUT_DIR / "magic_full_status.tsv"
    cols = ["path","status","syntax_ok","cov_pct","cov_covered","cov_total","lines","size_bytes","syntax_error"]
    with tsv.open("w", encoding="utf-8", newline="") as f:
        f.write("\t".join(cols)+"\n")
        for r in rows:
            def q(x):
                s = "" if x is None else str(x)
                return s.replace("\t"," ").replace("\r"," ").replace("\n"," ⏎ ")
            f.write("\t".join(q(r.get(c)) for c in cols)+"\n")

    # JSON
    (OUT_DIR / "magic_full_status.json").write_text(
        json.dumps({"summary": summary, "files": rows}, indent=2),
        encoding="utf-8"
    )

    print("=== MAGIC FAST STATUS ===")
    print(f"Root: {ROOT}")
    print(f"Files scanned: {totals['files']}")
    print(f"Real: {totals.get('real',0)} | Placeholder: {totals.get('placeholder',0)} | Empty: {totals.get('empty',0)} | Broken: {totals.get('broken',0)}")
    print(f"Coverage: {summary['coverage_overall_pct']}% (lines: {totals['covered_lines']}/{totals['total_lines']})")
    print(f"Wrote: {tsv}")
    print(f"Wrote: {OUT_DIR / 'magic_full_status.json'}")

if __name__ == "__main__":
    scan()
