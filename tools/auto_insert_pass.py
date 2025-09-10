import os
import re
import sys
import py_compile
import shutil
import time

ROOT = r"D:\MAGIC"
LIST = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(
    ROOT, "backups", f"auto_insert_pass_{time.strftime('%Y%m%d_%H%M%S')}"
)
os.makedirs(BACKUP, exist_ok=True)

CTRL_RE = re.compile(
    r"^\s*(if|elif|else|for|while|try|except|finally|def|class)\b.*:\s*(#.*)?$"
)


def needs_pass(lines, i):
    """Return True if line i is a control stmt and next non-empty line is not more-indented."""
    cur = lines[i]
    if not CTRL_RE.match(cur):
        return False
    cur_indent = len(cur) - len(cur.lstrip())
    # find next non-empty/non-comment
    j = i + 1
    while j < len(lines) and (
        lines[j].strip() == "" or lines[j].lstrip().startswith("#")
    ):
        j += 1
    if j >= len(lines):
        return True
    next_indent = len(lines[j]) - len(lines[j].lstrip())
    return next_indent <= cur_indent


def fix_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines(True)
    changed = False
    i = 0
    while i < len(lines):
        if needs_pass(lines, i):
            indent = " " * (len(lines[i]) - len(lines[i].lstrip()) + 4)
            lines.insert(i + 1, indent + "pass\n")
            changed = True
            i += 1
        i += 1
    if changed:
        dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)
    return changed


def main():
    if not os.path.exists(LIST):
        print("Missing compile_failures.tsv; run tools/list_compile_failures.py first.")
        sys.exit(0)
    fixed = 0
    with open(LIST, "r", encoding="utf-8") as f:
        next(f, None)  # header
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if not p or not p.endswith(".py") or not os.path.exists(p):
                continue
            try:
                py_compile.compile(p, doraise=True)
                continue
            except Exception:
                pass
            if fix_file(p):
                fixed += 1
    print(f"Inserted 'pass' in {fixed} files. Backups in {BACKUP}")


if __name__ == "__main__":
    main()
