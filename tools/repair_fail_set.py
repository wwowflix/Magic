#!/usr/bin/env python3
import sys  # noqa: I001
import ast
import re
import pathlib

FAIL_LIST = sys.argv[1] if len(sys.argv) > 1 else r".\outputs\reports\_fail_paths.txt"


def read_text(path):
    b = pathlib.Path(path).read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return b.decode(enc), enc
        except Exception:
            pass
    return b.decode("utf-8", "replace"), "utf-8"


def ast_ok(text, filename="<string>"):
    try:
        ast.parse(text, filename=filename)
        return True
    except Exception:
        return False


def write_utf8(path, text):
    pathlib.Path(path).write_text(text, encoding="utf-8")


MOJIBAKE = {
    "â€”": "—",
    "â€“": "–",
    "â€˜": "‘",
    "â€™": "’",
    "â€œ": "“",
    "â€�": "”",
    "â€¦": "…",
    "â€¢": "•",
    "â€¡": "‡",
    "â€": "”",
    "Ã—": "×",
    "ÃŸ": "ß",
    "Ã†": "Æ",
    "Ã˜": "Ø",
    "Ã¥": "å",
    "Ã¤": "ä",
    "Ã¶": "ö",
    "Ã¼": "ü",
    "Ã©": "é",
    "Ã¨": "è",
    "Ãª": "ê",
    "Ãº": "ú",
    "Ã³": "ó",
    "Ã²": "ò",
    "Ã­": "í",
    "Ã¡": "á",
    "Ã£": "ã",
    "Ãµ": "õ",
    "Ã¢": "â",
    "Ã´": "ô",
    "Ã§": "ç",
    "Ã¹": "ù",
    "Ã±": "ñ",
    "Â ": "",
    "Â": "",
    "â„¢": "™",
    "â‚¬": "€",
    "â€º": "›",
    "â€¹": "‹",
}


def demojibake(t):
    for bad, good in MOJIBAKE.items():
        if bad in t:
            t = t.replace(bad, good)
    t = re.sub(r"â€\s*", '"', t)
    return t.replace("Ã‚", "").replace("Ã", "")


def norm_nl(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return t if t.endswith("\n") else t + "\n"


def fix_triple_quotes(t):
    for q in ('"""', "'''"):
        if t.count(q) % 2 == 1:
            t += f"\n{q}"
    return t


def expand_tabs(t):
    return t.expandtabs(4)


def strip_nulls_bytes(path):
    b = pathlib.Path(path).read_bytes()
    if b.find(b"\x00") >= 0:
        b = b.replace(b"\x00", b"")
        try:
            return b.decode("utf-8")
        except Exception:
            return b.decode("latin-1", "replace")
    return None


def attempt(path):
    orig, _ = read_text(path)
    if ast_ok(orig, path):
        return None
    cands = []
    t = norm_nl(demojibake(orig.lstrip("\ufeff")))
    cands.append(t)
    cands.append(fix_triple_quotes(t))
    cands.append(expand_tabs(t))
    nfix = strip_nulls_bytes(path)
    if nfix is not None:
        cands.append(norm_nl(nfix))
    for cand in cands:
        if ast_ok(cand, path):
            return cand
    return None


def main():
    paths = [p for p in pathlib.Path(FAIL_LIST).read_text().splitlines() if p.strip()]
    fixed = 0
    still = 0
    for rel in paths:
        fs = pathlib.Path(rel)
        if not fs.exists() or fs.suffix != ".py":
            continue
        new = attempt(str(fs))
        if new is not None:
            write_utf8(str(fs), new)
            fixed += 1
            print("FIXED", rel)
        else:
            still += 1
            print("STILL_FAIL", rel)
    print(f"SUMMARY fixed={fixed} remaining={still}")


if __name__ == "__main__":
    main()
