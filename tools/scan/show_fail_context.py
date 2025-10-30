import pathlib

targets = [
    ("scripts/lexer.py", 194, 3),
    ("scripts/magic_dashboard.py", 191, 3),
    ("scripts/reddit_api_final.py", 38, 3),
    ("scripts/reddit_api_fixed.py", 38, 3),
    ("scripts/reddit_api_2.py", 38, 3),
]
for fn, ln, ctx in targets:
    p = pathlib.Path(fn)
    if not p.exists():
        print(f"MISS {fn}")
        continue
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    i = ln - 1
    a = max(0, i - ctx)
    b = min(len(lines), i + ctx + 1)
    print(f"\n==== {fn}:{ln} ({a+1}-{b}) ====")
    for n in range(a, b):
        print(f"{n+1:>6}: {lines[n]}")
