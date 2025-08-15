# 11C_script_integrity_checker_READY.py
import os
import sys
import ast

# repo root (works when run from anywhere, incl. tests)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

def list_ready_py(root):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith("_READY.py"):
                yield os.path.join(dirpath, fn)

def check_file(path):
    # 1) Non-empty file
    if os.path.getsize(path) == 0:
        return False, "empty file"

    # 2) UTF-8 (accept BOM) read
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            src = f.read()
    except Exception as e:
        return False, f"utf8-read-fail: {e}"

    # 3) Syntax check (no imports executed)
    try:
        ast.parse(src, filename=path)
    except SyntaxError as e:
        return False, f"syntax-error: {e}"

    return True, "ok"

def main():
    problems = []
    total = 0
    for p in list_ready_py(SCRIPTS_DIR):
        total += 1
        ok, msg = check_file(p)
        if not ok:
            problems.append((p, msg))

    if problems:
        print("INTEGRITY FAILURES:")
        for p, msg in problems:
            print(f"- {p}: {msg}")
        print(f"Checked={total} Fail={len(problems)}")
        sys.exit(1)

    print(f"Integrity OK. Checked={total} Fail=0")
    sys.exit(0)

if __name__ == "__main__":
    main()
