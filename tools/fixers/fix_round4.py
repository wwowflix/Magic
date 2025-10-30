#!/usr/bin/env python3
import pathlib  # noqa: I001
import re
import ast
import shutil

DIAG = r".\outputs\reports\magic_fail_diag_latest.tsv"

# explicit targets (file -> line) from your diag
TARGETS = {
    "scripts/lexer.py": 194,
    "scripts/magic_dashboard.py": 191,
    "scripts/reddit_api_final.py": 38,
    "scripts/reddit_api_fixed.py": 38,
    "scripts/reddit_api_2.py": 38,
}

OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
RE_UNTERM_STR = re.compile(r"unterminated string literal \(detected at line (\d+)\)")
RE_INVALID_SYNTAX = re.compile(r"invalid syntax.*line (\d+)")
RE_UNEXP_INDENT = re.compile(r"unexpected indent.*line (\d+)")


def ast_ok(txt: str) -> bool:
    try:
        ast.parse(txt)
        return True
    except Exception:
        return False


def read_text(p: pathlib.Path) -> str:
    b = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode("utf-8", "replace")


def write_backup_then(p: pathlib.Path, txt: str):
    if not txt.endswith("\n"):
        txt += "\n"
    shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
    p.write_text(txt, encoding="utf-8")


def normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def count_unescaped(line: str, q: str) -> int:
    i = 0
    c = 0
    while i < len(line):
        if line[i] == "\\":
            i += 2
            continue
        if line[i] == q:
            c += 1
        i += 1
    return c


def close_missing_quote(line: str) -> str:
    for q in ("'", '"'):
        if count_unescaped(line, q) % 2 == 1:
            s = line.rstrip()
            if s.endswith("\\"):
                s = s[:-1]
            return s + q
    return line


def balance_parens_on_line(line: str) -> str:
    out = []
    stack = []
    i = 0
    in_q = None
    while i < len(line):
        ch = line[i]
        if in_q:
            out.append(ch)
            if ch == "\\":
                i += 2
                continue
            if ch == in_q:
                in_q = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_q = ch
            out.append(ch)
        else:
            out.append(ch)
            if ch in OPEN_TO_CLOSE:
                stack.append(OPEN_TO_CLOSE[ch])
            elif ch in OPEN_TO_CLOSE.values() and stack and ch == stack[-1]:
                stack.pop()
        i += 1
    if stack:
        out.append("".join(reversed(stack)))
    return "".join(out)


def try_add_comma(line: str) -> str:
    s = line.rstrip()
    if s and not s.endswith((",", "(", "[", "{")):
        return s + ","
    return line


def fix_lexer_unterminated(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    new_line = close_missing_quote(lines[idx])
    if new_line != lines[idx]:
        lines[idx] = new_line
        cand = "\n".join(lines)
        if ast_ok(cand):
            write_backup_then(p, cand)
            return True
    # fallback: also try paren balance on same line
    cand_line = balance_parens_on_line(lines[idx])
    if cand_line != lines[idx]:
        lines[idx] = cand_line
        cand = "\n".join(lines)
        if ast_ok(cand):
            write_backup_then(p, cand)
            return True
    return False


def fix_dashboard_invalid(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    variants = []
    # quotes
    lq = close_missing_quote(lines[idx])
    if lq != lines[idx]:
        tmp = lines.copy()
        tmp[idx] = lq
        variants.append("\n".join(tmp))
    # parens
    lp = balance_parens_on_line(lines[idx])
    if lp != lines[idx]:
        tmp = lines.copy()
        tmp[idx] = lp
        variants.append("\n".join(tmp))
    # trailing comma
    lc = try_add_comma(lines[idx])
    if lc != lines[idx]:
        tmp = lines.copy()
        tmp[idx] = lc
        variants.append("\n".join(tmp))
    for cand in variants:
        if ast_ok(cand):
            write_backup_then(p, cand)
            return True
    return False


def fix_unexpected_indent(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    # find previous non-blank
    k = idx - 1
    while k >= 0 and lines[k].strip() == "":
        k -= 1
    if k < 0:
        return False
    prev = lines[k]
    prev_indent = len(prev) - len(prev.lstrip(" \t"))
    # desired: same indent as prev unless prev endswith ':', then prev+4
    desired = prev_indent + 4 if prev.rstrip().endswith(":") else prev_indent
    curr = lines[idx]
    stripped = curr.lstrip(" \t")
    # only reduce or align (avoid adding more indent)
    new = (" " * min(desired, prev_indent + 4)) + stripped if stripped else stripped
    # if prev doesn’t end with ':', force align to prev_indent (not deeper)
    if not prev.rstrip().endswith(":"):
        new = (" " * prev_indent) + stripped
    if new != curr:
        lines[idx] = new
        cand = "\n".join(lines)
        if ast_ok(cand):
            write_backup_then(p, cand)
            return True
    return False


def main():
    fixed = 0
    pending = 0
    for rel, ln in TARGETS.items():
        p = pathlib.Path(rel)
        if not p.exists():
            pending += 1
            continue
        if "lexer.py" in rel:
            ok = fix_lexer_unterminated(p, ln)
        elif "magic_dashboard.py" in rel:
            ok = fix_dashboard_invalid(p, ln)
        else:
            ok = fix_unexpected_indent(p, ln)
        if ok:
            fixed += 1
        else:
            pending += 1
    print(f"FIX_ROUND4 fixed={fixed} pending={pending}")


if __name__ == "__main__":
    main()
