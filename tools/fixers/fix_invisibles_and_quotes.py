#!/usr/bin/env python3
import ast
import pathlib
import re

FAIL_LIST = r".\outputs\reports\_fail_paths.txt"

SMART = {
    "–": "-",
    "—": "-",
    "…": "...",
    "“": '"',
    "”": '"',
    "„": '"',
    "‟": '"',
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
}
CTRL_RE = re.compile(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]")
ZWS_RE = re.compile(r"[\u200B-\u200F\u202A-\u202E]")  # zero-width & bidi
NBSP_RE = re.compile(r"\u00A0")  # nbsp
SHY_RE = re.compile(r"\u00AD")  # soft hyphen
BOM_RE = re.compile(r"^\ufeff")


def ast_ok(s, fn):
    try:
        ast.parse(s, filename=fn)
        return True
    except Exception:
        return False


def normalize_text(txt: str) -> str:
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    txt = BOM_RE.sub("", txt)
    txt = CTRL_RE.sub("", txt)
    txt = ZWS_RE.sub("", txt)
    txt = NBSP_RE.sub(" ", txt)
    txt = SHY_RE.sub("", txt)
    for bad, good in SMART.items():
        if bad in txt:
            txt = txt.replace(bad, good)
    return txt


def balance_simple_quotes_line(line: str) -> str:
    # Skip lines that look like triple-quoted blocks or end with backslash
    if '"""' in line or "'''" in line or line.rstrip().endswith("\\"):
        return line
    dq = line.count('"') - line.count('\\"')
    sq = line.count("'") - line.count("\\'")
    # Heuristic: if one of them is odd, append the matching quote
    if dq % 2 == 1 and sq % 2 == 0:
        return line + '"'
    if sq % 2 == 1 and dq % 2 == 0:
        return line + "'"
    return line


def try_line_quote_balance(txt: str) -> str:
    lines = txt.split("\n")
    changed = False
    for i, ln in enumerate(lines):
        new = balance_simple_quotes_line(ln)
        if new != ln:
            lines[i] = new
            changed = True
    return "\n".join(lines) if changed else txt


def load_text(path: pathlib.Path) -> str:
    b = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode("utf-8", "replace")


def process_file(p: pathlib.Path) -> bool:
    orig = load_text(p)
    if ast_ok(orig, str(p)):
        return False

    t = normalize_text(orig)
    if t != orig and ast_ok(t, str(p)):
        p.write_text(t, encoding="utf-8")
        return True

    # If still failing, try balancing simple quotes per-line
    t2 = try_line_quote_balance(t)
    if t2 != t and ast_ok(t2, str(p)):
        p.write_text(t2, encoding="utf-8")
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
    print(f"FIX_INVISIBLES_QUOTES fixed={fixed} still={still}")


if __name__ == "__main__":
    main()
