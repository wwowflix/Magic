#!/usr/bin/env python3
import ast  # noqa: I001
import pathlib
import shutil
import tokenize
import io

TARGETS = {
    "scripts/lexer.py": 194,
    "scripts/magic_dashboard.py": 191,
    "scripts/reddit_api_final.py": 38,
    "scripts/reddit_api_fixed.py": 38,
    "scripts/reddit_api_2.py": 38,
}

OPEN2CLOSE = {"(": ")", "[": "]", "{": "}"}
SMART = {"“": '"', "”": '"', "„": '"', "‟": '"', "‘": "'", "’": "'", "‚": "'", "‛": "'"}


def ast_ok(s: str) -> bool:
    try:
        ast.parse(s)
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


def norm(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    lines = []
    for ln in s.split("\n"):
        head = ln[: len(ln) - len(ln.lstrip())]
        body = ln[len(head) :]
        head = head.replace("\u00a0", " ").expandtabs(4)
        head = "".join(" " if ch in " \t" else "" for ch in head)
        body = body.replace("\u00a0", " ")
        lines.append(head + body)
    s = "\n".join(lines)
    for bad, good in SMART.items():
        s = s.replace(bad, good)
    return s


def in_string_at_line(source: str, line_no: int) -> bool:
    try:
        stoks = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except tokenize.TokenError:
        return False
    # build string spans
    str_spans = []
    for tok in stoks:
        ttype, tstr, (srow, _), (erow, _), _ = tok
        if ttype == tokenize.STRING:
            str_spans.append((srow, erow))
    for a, b in str_spans:
        if a <= line_no <= b:
            return True
    return False


def close_string_on_line(line: str) -> str:
    # close the currently open quote type if odd count (ignore escaped)
    def count_unescaped(s, q):
        i = 0
        c = 0
        while i < len(s):
            if s[i] == "\\":
                i += 2
                continue
            if s[i] == q:
                c += 1
            i += 1
        return c

    for q in ("'", '"'):
        if count_unescaped(line, q) % 2 == 1:
            s = line.rstrip()
            if s.endswith("\\"):
                s = s[:-1]
            return s + q
    return line


def balance_parens(line: str) -> str:
    out = []
    stack = []
    i = 0
    q = None
    while i < len(line):
        ch = line[i]
        out.append(ch)
        if q:
            if ch == "\\":
                i += 2
                continue
            if ch == q:
                q = None
        else:
            if ch in ("'", '"'):
                q = ch
            elif ch in OPEN2CLOSE:
                stack.append(OPEN2CLOSE[ch])
            elif stack and ch == stack[-1]:
                stack.pop()
        i += 1
    if stack:
        out.append("".join(reversed(stack)))
    return "".join(out)


def try_trailing_comma(line: str) -> str:
    s = line.rstrip()
    if s and s[-1] not in ",([{":
        return s + ","
    return line


def fix_unexpected_indent_one_line(txt: str, idx: int) -> str | None:
    lines = txt.split("\n")
    if not (0 <= idx < len(lines)):
        return None
    stripped = lines[idx].lstrip(" ")
    # aggressive: force top-level indent for that line only
    cand = "\n".join([(stripped if j == idx else ln) for j, ln in enumerate(lines)])
    if ast_ok(cand):
        return cand
    # plan B: align to previous nonblank indent or +4 if prev endswith ':'
    k = idx - 1
    while k >= 0 and lines[k].strip() == "":
        k -= 1
    if k >= 0:
        prev = lines[k]
        prev_indent = len(prev) - len(prev.lstrip(" "))
        want = prev_indent + (4 if prev.rstrip().endswith(":") else 0)
        cand2 = "\n".join(
            [
                ((" " * want) + stripped if j == idx else ln)
                for j, ln in enumerate(lines)
            ]
        )
        if ast_ok(cand2):
            return cand2
    return None


def patch_file(p: pathlib.Path, line_no: int) -> bool:
    raw = read_text(p)
    txt = norm(raw)
    if ast_ok(txt):
        return False

    lines = txt.split("\n")
    i = line_no - 1
    if not (0 <= i < len(lines)):
        return False

    variants = []

    if p.name.startswith("reddit_api_"):
        v = fix_unexpected_indent_one_line(txt, i)
        if v:
            variants.append(v)

    elif p.name == "lexer.py":
        # if tokenizer says we are inside a string at/near line, close + balance
        for d in (0, 1, 2):
            tlines = lines.copy()
            j = min(len(lines) - 1, max(0, i + d))
            if in_string_at_line(txt, j + 1):
                tlines[j] = balance_parens(close_string_on_line(tlines[j]))
            else:
                tlines[j] = balance_parens(tlines[j])
            variants.append("\n".join(tlines))

    elif p.name == "magic_dashboard.py":
        # try multiple combos
        for mut in (close_string_on_line, try_trailing_comma, balance_parens):
            v = lines.copy()
            v[i] = mut(v[i])
            variants.append("\n".join(v))
        v = lines.copy()
        v[i] = balance_parens(try_trailing_comma(close_string_on_line(v[i])))
        variants.append("\n".join(v))

    # also try global “close dangling triple quotes” if any
    for q in ('"""', "'''"):
        if txt.count(q) % 2 == 1:
            v = txt + ("\n" + q + "\n")
            variants.append(v)

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
        if patch_file(p, ln):
            fixed += 1
        else:
            pending += 1
    print(f"FIX_ROUND6 fixed={fixed} pending={pending}")


if __name__ == "__main__":
    main()
