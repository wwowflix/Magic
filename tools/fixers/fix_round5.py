#!/usr/bin/env python3
import ast
import pathlib
import shutil

TARGETS = {
    "scripts/lexer.py": 194,
    "scripts/magic_dashboard.py": 191,
    "scripts/reddit_api_final.py": 38,
    "scripts/reddit_api_fixed.py": 38,
    "scripts/reddit_api_2.py": 38,
}

OPEN2CLOSE = {"(": ")", "[": "]", "{": "}"}
SMART = {"“": '"', "”": '"', "„": '"', "‟": '"', "‘": "'", "’": "'", "‚": "'", "‛": "'"}


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
    shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
    if not txt.endswith("\n"):
        txt += "\n"
    p.write_text(txt, encoding="utf-8")


def norm_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def norm_invisibles(s: str) -> str:
    # normalize leading whitespace on every line: tabs->4 spaces, strip NBSP and control Zs  # noqa: E501
    out = []
    for ln in s.split("\n"):
        head = ln[: len(ln) - len(ln.lstrip())]
        tail = ln[len(head) :]
        head = head.replace("\u00a0", " ")  # NBSP
        head = head.expandtabs(4)
        head = "".join((" " if (ch == " " or ch == "\t") else "") for ch in head)
        # collapse weird invisibles in body too
        tail = tail.replace("\u00a0", " ")
        out.append(head + tail)
    s = "\n".join(out)
    # smart quotes → ascii
    for bad, good in SMART.items():
        s = s.replace(bad, good)
    return s


def count_unescaped(line, q):
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


def balance_parens(line: str) -> str:
    stack = []
    out = []
    i = 0
    inq = None
    while i < len(line):
        ch = line[i]
        if inq:
            out.append(ch)
            if ch == "\\":
                i += 2
                continue
            if ch == inq:
                inq = None
            i += 1
            continue
        if ch in ("'", '"'):
            inq = ch
            out.append(ch)
        else:
            out.append(ch)
            if ch in OPEN2CLOSE:
                stack.append(OPEN2CLOSE[ch])
            elif stack and ch == stack[-1]:
                stack.pop()
        i += 1
    if stack:
        out.append("".join(reversed(stack)))
    return "".join(out)


def try_trailing_comma(line: str) -> str:
    s = line.rstrip()
    if s and not s.endswith((",", "(", "[", "{")):
        return s + ","
    return line


def fix_unexpected_indent(full: str, idx: int) -> str | None:
    lines = full.split("\n")
    k = idx - 1
    while k >= 0 and lines[k].strip() == "":
        k -= 1
    if k < 0:
        return None
    prev = lines[k]
    prev_indent = len(prev) - len(prev.lstrip(" "))
    curr = lines[idx]
    stripped = curr.lstrip(" ")
    want = prev_indent + (4 if prev.rstrip().endswith(":") else 0)
    new = (" " * want) + stripped
    if new != curr:
        lines[idx] = new
        cand = "\n".join(lines)
        if ast_ok(cand):
            return cand
    # second chance: align exactly to prev indent if above failed
    new = (" " * prev_indent) + stripped
    if new != curr:
        lines[idx] = new
        cand = "\n".join(lines)
        if ast_ok(cand):
            return cand
    return None


def patch_file(p: pathlib.Path, line_no: int) -> bool:
    txt = norm_newlines(read_text(p))
    if ast_ok(txt):
        return False
    txt = norm_invisibles(txt)
    lines = txt.split("\n")
    i = line_no - 1
    if not (0 <= i < len(lines)):
        return False

    variants = []

    if p.name == "lexer.py":
        v = lines.copy()
        v[i] = close_missing_quote(v[i])
        variants.append("\n".join(v))
        v = lines.copy()
        v[i] = balance_parens(v[i])
        variants.append("\n".join(v))

    elif p.name == "magic_dashboard.py":
        for mut in (close_missing_quote, balance_parens, try_trailing_comma):
            v = lines.copy()
            v[i] = mut(v[i])
            variants.append("\n".join(v))
        # try combo: quote → comma → paren
        v = lines.copy()
        v[i] = balance_parens(try_trailing_comma(close_missing_quote(v[i])))
        variants.append("\n".join(v))

    else:  # reddit_* unexpected indent
        cand = fix_unexpected_indent(txt, i)
        if cand:
            variants.append(cand)

    for cand in variants:
        if cand != txt and ast_ok(cand):
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
        ok = patch_file(p, ln)
        if ok:
            fixed += 1
        else:
            pending += 1
    print(f"FIX_ROUND5 fixed={fixed} pending={pending}")


if __name__ == "__main__":
    main()
