#!/usr/bin/env python3
import ast
import pathlib
import re

FAIL_LIST = r".\outputs\reports\_fail_paths.txt"

REPL_LINE = re.compile(r"^(>>> |\.\.\. )")  # strip Python REPL prompts


def ast_ok(s, fn):
    try:
        ast.parse(s, filename=fn)
        return True
    except Exception:
        return False


def load_text(p: pathlib.Path) -> str:
    b = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode("utf-8", "replace")


def strip_repl_and_fix_backslash(txt: str) -> str:
    # normalize newlines
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    # strip REPL prompts at line starts
    lines = [REPL_LINE.sub("", ln) for ln in txt.split("\n")]
    # remove a single dangling trailing backslash at EOF
    i = len(lines) - 1
    # skip trailing blank lines to find the last real line
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    if i >= 0 and lines[i].rstrip().endswith("\\"):
        lines[i] = lines[i].rstrip()[:-1]
    out = "\n".join(lines)
    if not out.endswith("\n"):
        out += "\n"
    return out


def process_file(p: pathlib.Path) -> bool:
    orig = load_text(p)
    if ast_ok(orig, str(p)):
        return False
    t = strip_repl_and_fix_backslash(orig)
    if t != orig and ast_ok(t, str(p)):
        p.write_text(t, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    still = 0
    for rel in pathlib.Path(FAIL_LIST).read_text().splitlines():
        fp = pathlib.Path(rel)
        if not fp.is_file():
            continue
        if process_file(fp):
            fixed += 1
        else:
            still += 1
    print(f"FIX_REPL_BACKSLASH fixed={fixed} still={still}")


if __name__ == "__main__":
    main()
