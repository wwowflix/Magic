#!/usr/bin/env python3
# Targeted round-3 fixer for 6 remaining files based on your diag.

import csv  # noqa: I001
import pathlib
import re
import ast
import shutil

DIAG = r".\outputs\reports\magic_fail_diag_latest.tsv"

RE_UNTERM_STR = re.compile(r"unterminated string literal \(detected at line (\d+)\)")
RE_PAREN_NEVER = re.compile(r"'\(' was never closed.*line (\d+)\)")
RE_UNEXP_INDENT = re.compile(r"unexpected indent.*line (\d+)")
RE_INVALID_SYNTAX = re.compile(r"invalid syntax.*line (\d+)")

OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}


def ast_ok(txt, fn):
    try:
        ast.parse(txt)
        return True
    except Exception:
        return False


def read_text(p: pathlib.Path):
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
    # Count (), [], {} ignoring quoted segments
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
    # Heuristic: if line looks like item/kv in a literal, try a trailing comma
    s = line.rstrip()
    if not s.endswith((",", "(", "[", "{")) and s:
        return s + ","
    return line


def normalize_newlines(txt: str) -> str:
    return txt.replace("\r\n", "\n").replace("\r", "\n")


def fix_unterminated_string_at(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    new_line = close_missing_quote(lines[idx])
    if new_line != lines[idx]:
        lines[idx] = new_line
        new_txt = "\n".join(lines)
        if ast_ok(new_txt, str(p)):
            write_backup_then(p, new_txt)
            return True
    return False


def fix_paren_never_closed_at(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    cand = balance_parens_on_line(lines[idx])
    if cand != lines[idx]:
        lines[idx] = cand
        new_txt = "\n".join(lines)
        if ast_ok(new_txt, str(p)):
            write_backup_then(p, new_txt)
            return True
    return False


def fix_invalid_syntax_try_comma_at(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    variants = []

    # 1) close quotes
    v1 = lines[idx]
    v1c = close_missing_quote(v1)
    if v1c != v1:
        tmp = lines.copy()
        tmp[idx] = v1c
        variants.append("\n".join(tmp))

    # 2) balance parens
    v2 = lines[idx]
    v2c = balance_parens_on_line(v2)
    if v2c != v2:
        tmp = lines.copy()
        tmp[idx] = v2c
        variants.append("\n".join(tmp))

    # 3) add trailing comma
    v3 = lines[idx]
    v3c = try_add_comma(v3)
    if v3c != v3:
        tmp = lines.copy()
        tmp[idx] = v3c
        variants.append("\n".join(tmp))

    for cand in variants:
        if ast_ok(cand, str(p)):
            write_backup_then(p, cand)
            return True
    return False


def fix_unexpected_indent_at(p: pathlib.Path, ln: int) -> bool:
    txt = normalize_newlines(read_text(p))
    lines = txt.split("\n")
    idx = ln - 1
    if not (0 <= idx < len(lines)):
        return False
    # prev non-blank
    k = idx - 1
    while k >= 0 and lines[k].strip() == "":
        k -= 1
    if k < 0:
        return False
    prev = lines[k]
    prev_indent = len(prev) - len(prev.lstrip(" \t"))
    target = lines[idx]
    target_stripped = target.lstrip(" \t")
    # If previous line ends with ":", keep at prev_indent+4, else align to prev_indent
    desired = prev_indent + 4 if prev.rstrip().endswith(":") else prev_indent
    new_line = (" " * desired) + target_stripped
    if new_line != target:
        lines[idx] = new_line
        new_txt = "\n".join(lines)
        if ast_ok(new_txt, str(p)):
            write_backup_then(p, new_txt)
            return True
    return False


def main():
    fixed = 0
    pending = 0
    with open(DIAG, encoding="utf-8") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for row in rd:
            if row.get("status") != "FAIL":
                continue
            p = pathlib.Path(row["path"])
            row.get("diag_type", "")
            dm = row.get("diag_msg", "")

            # cost_guard_2: '(' never closed
            m = RE_PAREN_NEVER.search(dm)
            if m:
                ln = int(m.group(1))
                if fix_paren_never_closed_at(p, ln):
                    fixed += 1
                else:
                    pending += 1
                continue

            # unterminated string
            m = RE_UNTERM_STR.search(dm)
            if m:
                ln = int(m.group(1))
                if fix_unterminated_string_at(p, ln):
                    fixed += 1
                else:
                    pending += 1
                continue

            # unexpected indent
            m = RE_UNEXP_INDENT.search(dm)
            if m:
                ln = int(m.group(1))
                if fix_unexpected_indent_at(p, ln):
                    fixed += 1
                else:
                    pending += 1
                continue

            # invalid syntax (try comma / quotes / parens)
            m = RE_INVALID_SYNTAX.search(dm)
            if m:
                ln = int(m.group(1))
                if fix_invalid_syntax_try_comma_at(p, ln):
                    fixed += 1
                else:
                    pending += 1
                continue

            pending += 1

    print(f"FIX_ROUND3 fixed={fixed} pending={pending}")


if __name__ == "__main__":
    main()
