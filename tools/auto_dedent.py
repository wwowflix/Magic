import os
import time
import shutil
import py_compile

ROOT = r"D:\MAGIC"
LIST = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(ROOT, "backups", f"auto_dedent_{time.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP, exist_ok=True)


def compiles(p):
    try:
        py_compile.compile(p, doraise=True)
        return True
    except Exception:
        return False


def dedent_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    changed = False
    # Try to gently reduce excessive leading indentation in the first ~200 lines
    limit = min(200, len(lines))
    for i in range(limit):
        # Skip empty/comment lines
        s = lines[i]
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        # If a line starts with 8+ spaces but previous non-empty had less indent, trim 4
        cur_indent = len(s) - len(s.lstrip(" "))
        if cur_indent >= 8:
            lines[i] = s[4:]  # remove one level
            changed = True

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
        return
    with open(LIST, "r", encoding="utf-8") as f:
        next(f, None)  # header
        targets = []
        for line in f:
            parts = line.rstrip("\n").split("\t", 1)
            if not parts:
                continue
            p = parts[0]
            if not p.endswith(".py") or not os.path.exists(p):
                continue
            # Only process files currently failing to compile
            if not compiles(p):
                targets.append(p)

    fixed = 0
    for p in targets:
        if dedent_file(p) and compiles(p):
            fixed += 1
    print(f"Dedent pass complete. Fixed & compiling: {fixed}/{len(targets)}")
    print("Backups:", BACKUP)


if __name__ == "__main__":
    main()
