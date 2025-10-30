#!/usr/bin/env python3
import ast
import pathlib

fail_list = r".\outputs\reports\_fail_paths.txt"

SMART = {
    "“": '"',
    "”": '"',
    "„": '"',
    "‟": '"',
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
    "‹": "<",
    "›": ">",
    "«": "<<",
    "»": ">>",
}
PAIRS = {"(": ")", "[": "]", "{": "}"}


def ast_ok(txt, fn):
    try:
        ast.parse(txt, filename=fn)
        return True
    except Exception:
        return False


def normalize_quotes(txt):
    for bad, good in SMART.items():
        if bad in txt:
            txt = txt.replace(bad, good)
    return txt


def balance_pairs(txt):
    stack = []
    for ch in txt:
        if ch in PAIRS:
            stack.append(PAIRS[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
    if stack:
        txt = txt.rstrip() + "".join(reversed(stack)) + "\n"
    return txt


def close_unterminated_triple_quotes(txt):
    for q in ('"""', "'''"):
        if txt.count(q) % 2 == 1:
            txt = txt.rstrip() + f"\n{q}\n"
    return txt


def run_one(p: pathlib.Path):
    t = p.read_text(encoding="utf-8", errors="replace")
    if ast_ok(t, str(p)):
        return False
    t1 = t.replace("\r\n", "\n").replace("\r", "\n")
    t1 = normalize_quotes(t1)
    t1 = close_unterminated_triple_quotes(t1)
    t1 = balance_pairs(t1)
    if t1 != t and ast_ok(t1, str(p)):
        p.write_text(t1, encoding="utf-8")
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
    print(f"FIX_QUOTES_PARENS fixed={fixed} still={still}")


if __name__ == "__main__":
    main()
