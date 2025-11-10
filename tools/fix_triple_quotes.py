import pathlib

root = pathlib.Path(".")
fixed = 0
for p in root.rglob("*.py"):
    t = p.read_text(errors="ignore")
    if "EOL while scanning string literal" in open(p, "rb").read().decode(
        "utf-8", "ignore"
    ):
        # not meaningful; we only need to patch strings, so skip this check
        pass
    # Detect odd count of triple quotes
    if t.count('"""') % 2 == 1:
        t += '\n"""'
        p.write_text(t, encoding="utf-8")
        fixed += 1
print(f"✅ Added closing triple quotes to {fixed} files")
