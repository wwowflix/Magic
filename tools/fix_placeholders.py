ï»¿import pathlib, re

roots = [
    "backups\\phase11", "backups\\phase11_cleanup",
    "backups\\phase11_final", "backups\\phase11_full_backup",
    "backups\\phase11_pre_rebuild",
]

def fix_file(p: pathlib.Path) -> bool:
    txt = p.read_text(errors="ignore")
    orig = txt

    # unescape triple quotes
    txt = txt.replace('\\"""', '"""').replace('\"\"\"', '"""')

    # normalize any docstring lines like: """ Placeholder for X """
    txt = re.sub(r'"""\\s*Placeholder\\s+for\\s+([^"]*?)\\s*"""',
                 lambda m: f'""" Placeholder for {m.group(1).strip()} """',
                 txt, flags=re.IGNORECASE)

    # normalize newlines to LF
    txt = txt.replace("\r\n", "\n")
    if txt != orig:
        p.write_text(txt, encoding="utf-8")
        return True
    return False

changed = 0
for root in roots:
    r = pathlib.Path(root)
    if not r.exists():
        continue
    for py in r.rglob("*.py"):
        try:
            if fix_file(py):
                changed += 1
        except Exception:
            pass

print(f"âœ… Placeholder/docstring fixes applied to {changed} files.")
"""
