#!/usr/bin/env python3
import ast
import pathlib

fail_list = r".\outputs\reports\_fail_paths.txt"


def ast_ok(s, fn):
    try:
        ast.parse(s, filename=fn)
        return True
    except Exception:
        return False


def normalize_indent_bytes(path: pathlib.Path):
    b = path.read_bytes()
    b = b.replace(b"\x00", b"")  # strip NULs
    try:
        s = b.decode("utf-8-sig")
    except Exception:
        s = b.decode("latin-1")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = s.expandtabs(4)
    if not s.endswith("\n"):
        s += "\n"
    return s


def run_one(p: pathlib.Path):
    s = normalize_indent_bytes(p)
    if ast_ok(s, str(p)):
        p.write_text(s, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    still = 0
    for rel in pathlib.Path(fail_list).read_text().splitlines():
        q = pathlib.Path(rel)
        if not q.is_file():
            continue
        if run_one(q):
            fixed += 1
        else:
            still += 1
    print(f"FIX_INDENT fixed={fixed} still={still}")


if __name__ == "__main__":
    main()
