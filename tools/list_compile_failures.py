import os, csv, py_compile, pathlib

ROOT = r"D:\MAGIC"
SCRIPTS = os.path.join(ROOT, "scripts")
OUTDIR = os.path.join(ROOT, "outputs", "reports")
os.makedirs(OUTDIR, exist_ok=True)
OUT = os.path.join(OUTDIR, "compile_failures.tsv")

rows = [("Path", "Error")]
for p in pathlib.Path(SCRIPTS).rglob("*.py"):
    p = p.resolve()
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as e:
        rows.append((str(p), f"{type(e).__name__}: {e}"))

with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerows(rows)

print(f"Wrote {OUT} with {len(rows)-1} failures")
