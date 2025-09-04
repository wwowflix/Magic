import re
import sys
import pathlib


def fix_print_py2(code: str) -> str:
    return re.sub(r"(?m)^\s*print\s+([^(\n]+)$", r"print(\1)", code)


def ensure_import(code: str, mod: str) -> str:
    return code if f"import {mod}" in code else f"import {mod}\n" + code


def main(path):
    p = pathlib.Path(path)
    s = p.read_text(encoding="utf-8")
    s2 = ensure_import(fix_print_py2(s), "sys")
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("patched", p)
    else:
        print("no changes", p)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        main(f)
