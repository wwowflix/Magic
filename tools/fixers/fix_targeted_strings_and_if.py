#!/usr/bin/env python3
# Heuristic + conservative:
# - Close single-line unterminated ' or " (skips triple quotes).
# - Insert "pass" for empty `if ...:` blocks.
# - Writes a .bak alongside each edited file.

import ast
import pathlib
import re
import shutil

TARGETS = {
    "scripts/cost_guard_2.py",
    "scripts/core.py",
    "scripts/lexer.py",
    "scripts/magic_dashboard.py",
    "scripts/python_parser.py",
    "scripts/reddit_api_2.py",
    "scripts/reddit_api_final.py",
    "scripts/reddit_api_fixed.py",
}

REPL_PROMPT = re.compile(r"^(>>> |\.\.\. )")
TRIPLE = ('"""', "'''")


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


def count_unescaped(line, qchar):
    i = 0
    c = 0
    while i < len(line):
        if line[i] == "\\":
            i += 2
            continue
        if line[i] == qchar:
            c += 1
        i += 1
    return c


def close_unterminated_quotes(lines):
    """Close single-line unterminated ' or " (skip lines that contain triple quotes)."""
    out = []
    for ln in lines:
        line = ln
        if any(t in line for t in TRIPLE):
            out.append(line)
            continue
        # Only act if the line by itself is the issue; add matching quote if odd count
        for q in ("'", '"'):
            if count_unescaped(line, q) % 2 == 1:
                line = line + q
        out.append(line)
    return out


def fix_empty_if_blocks(lines):
    """Insert 'pass' after lines matching `^\s*if ...:\s*$` when the next logical line isn't indented."""  # noqa: E501, W605
    out = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        out.append(ln)
        if re.match(r"^\s*if\b.+:\s*$", ln):
            # find next non-empty line index j
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            # if file ended OR next line is not more indented, insert 'pass'
            if j == n:
                out.append("    pass")
            else:
                curr_indent = len(ln) - len(ln.lstrip(" \t"))
                next_indent = len(lines[j]) - len(lines[j].lstrip(" \t"))
                if next_indent <= curr_indent:
                    out.append("    pass")
        i += 1
    return out


def normalize_common(txt: str) -> str:
    txt = txt.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    # strip REPL prompts if any leaked
    txt = "\n".join(REPL_PROMPT.sub("", ln) for ln in txt.split("\n"))
    if not txt.endswith("\n"):
        txt += "\n"
    return txt


def process_one(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    original = load_text(path)
    if ast_ok(original, str(path)):
        return False

    txt = normalize_common(original)
    lines = txt.split("\n")

    # 1) close quotes
    lines1 = close_unterminated_quotes(lines)
    txt1 = "\n".join(lines1)
    if ast_ok(txt1, str(path)):
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(txt1, encoding="utf-8")
        return True

    # 2) fix empty if blocks
    lines2 = fix_empty_if_blocks(lines1)
    txt2 = "\n".join(lines2)
    if ast_ok(txt2, str(path)):
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(txt2, encoding="utf-8")
        return True

    # 3) try both changes committed even if still failing (rare): write only if improves AST  # noqa: E501
    if txt2 != original and ast_ok(txt2, str(path)):
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(txt2, encoding="utf-8")
        return True

    return False


def main():
    fixed = 0
    still = []
    for rel in sorted(TARGETS):
        p = pathlib.Path(rel)
        if process_one(p):
            fixed += 1
        else:
            still.append(rel)
    print(f"FIX_TARGETS fixed={fixed} remaining={len(still)}")
    if still:
        print("REMAINING:")
        for s in still:
            print(" -", s)


if __name__ == "__main__":
    main()
