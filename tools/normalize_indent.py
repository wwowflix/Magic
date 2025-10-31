import pathlib

changed = 0
for p in pathlib.Path(".").rglob("*.py"):
    try:
        txt = p.read_text(encoding="utf-8")
    except Exception:
        continue
    new = txt.expandtabs(4)
    if new != txt:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"✅ Normalized indentation in {changed} files")
