#!/usr/bin/env python3
# Fix from diag: closes unterminated quotes at the reported line,
# and inserts an indented "pass" for empty `if:` blocks at the reported line.

import csv  # noqa: I001
import re
import pathlib
import shutil

DIAG = r".\outputs\reports\magic_fail_diag_latest.tsv"

RE_UNTERM = re.compile(r"unterminated string literal \(detected at line (\d+)\)")
RE_INDENT = re.compile(r"expected an indented block after 'if' statement on line (\d+)")


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
    # If odd number of single/double quotes (unescaped), add the closing one.
    for q in ("'", '"'):
        if count_unescaped(line, q) % 2 == 1:
            # trim a dangling trailing backslash if present
            s = line.rstrip()
            if s.endswith("\\"):
                s = s[:-1]
            return s + q
    return line


def insert_pass_after_if(lines, if_lineno):
    # if_lineno is 1-based
    idx = if_lineno - 1
    if idx < 0 or idx >= len(lines):
        return False
    ln = lines[idx]
    # Determine indentation on the `if` line
    indent = len(ln) - len(ln.lstrip(" \t"))
    pass_line = " " * (indent + 4) + "pass"
    # Insert immediately after, unless next line already more indented non-blank
    j = idx + 1
    # find first non-blank lookahead
    k = j
    while k < len(lines) and lines[k].strip() == "":
        k += 1
    need_insert = True
    if k < len(lines):
        next_indent = len(lines[k]) - len(lines[k].lstrip(" \t"))
        if next_indent > indent:
            need_insert = False
    if need_insert:
        lines.insert(j, pass_line)
        return True
    return False


def fix_unterminated(path: pathlib.Path, lineno: int) -> bool:
    txt = (
        path.read_text(encoding="utf-8", errors="replace")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )
    lines = txt.split("\n")
    idx = lineno - 1
    if idx < 0 or idx >= len(lines):
        return False
    new_line = close_missing_quote(lines[idx])
    if new_line != lines[idx]:
        lines[idx] = new_line
        new_txt = "\n".join(lines)
        # ensure trailing newline
        if not new_txt.endswith("\n"):
            new_txt += "\n"
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(new_txt, encoding="utf-8")
        return True
    return False


def fix_indent_if(path: pathlib.Path, lineno: int) -> bool:
    txt = (
        path.read_text(encoding="utf-8", errors="replace")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )
    lines = txt.split("\n")
    changed = insert_pass_after_if(lines, lineno)
    if changed:
        new_txt = "\n".join(lines)
        if not new_txt.endswith("\n"):
            new_txt += "\n"
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
        path.write_text(new_txt, encoding="utf-8")
    return changed


def main():
    fixed = 0
    pending = 0
    with open(DIAG, encoding="utf-8") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for row in rd:
            if row.get("status") != "FAIL":
                continue
            p = pathlib.Path(row["path"])
            diag_type = row.get("diag_type", "")
            diag_msg = row.get("diag_msg", "")
            if diag_type == "SyntaxError":
                m = RE_UNTERM.search(diag_msg)
                if m:
                    ln = int(m.group(1))
                    if fix_unterminated(p, ln):
                        fixed += 1
                    else:
                        pending += 1
                else:
                    pending += 1
            elif diag_type == "IndentationError":
                m = RE_INDENT.search(diag_msg)
                if m:
                    ln = int(m.group(1))
                    if fix_indent_if(p, ln):
                        fixed += 1
                    else:
                        pending += 1
                else:
                    pending += 1
            else:
                pending += 1
    print(f"FIX_FROM_DIAG fixed={fixed} pending={pending}")


if __name__ == "__main__":
    main()
