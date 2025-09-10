import os
import re
import time
import shutil
import csv
import py_compile

ROOT = r"D:\MAGIC"
LIST = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(
    ROOT, "backups", f"fix_quotes_hard_{time.strftime('%Y%m%d_%H%M%S')}"
)
OUT = os.path.join(ROOT, "outputs", "reports", "fix_quotes_hard_report.tsv")
os.makedirs(BACKUP, exist_ok=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Remove/control/sanitize common trouble chars
SANITIZE = {
    **{chr(c): "" for c in range(0x80, 0xA0)},  # U+0080..U+009F -> remove
    "\ufeff": "",
    "ÃƒÆ’Ã¢â‚¬Å¡": "",
    "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸": "",
    "ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢": "'",
    "ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“": '"',
    "ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¯Ã‚Â¿Ã‚Â½": '"',
    "ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ": "-",
    "ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â": "-",
    "Ãƒâ€šÃ‚Â¤": "",
    "Ãƒâ€šÃ‚Â¨": "",
    "Ãƒâ€šÃ‚Â®": "",
    "Ãƒâ€šÃ‚Â°": "",
    "Ãƒâ€šÃ‚Â³": "",
    "Ãƒâ€šÃ‚Â´": "",
    "Ãƒâ€šÃ‚Â¸": "",
    "Ãƒâ€šÃ‚Â¹": "",
    "ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¹": "",
    "ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬": "ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬",
    "ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢": "TM",
}

RX_F_TRIPLE_OPEN = re.compile(r'(\bf)\s*"""+')  # f"""" -> f"
RX_PRINT_TRIPLE_OPEN = re.compile(r'(\bprint\s*\()\s*"""+')  # print(""" -> print("
RX_RUN_4PLUS = re.compile(r'"{4,}')  # any run >=4 -> """
RX_TRIPLE_KEEP = re.compile(r'"""')  # protect triples temporarily
RX_RUN_2 = re.compile(r'(?<!")""(?!")')  # exact two-quote runs
RX_IDX_DBL_QUOTED = re.compile(
    r'\[""\s*([^"\]]+?)\s*""\]'
)  # [""author""] -> ["author"]
RX_EQ_DBL_QUOTE_L = re.compile(r'=\s*""')  # = "" -> = "
RX_DBL_QUOTE_R = re.compile(r'""\s*([,\)\]\}])')  # ""), ""] -> "), "]
RX_ALPHABET = re.compile(r'^\s*alphabet\s*=\s*"(.*)"\s*,?\s*$', re.UNICODE)
RX_ORD_EMPTY = re.compile(r'ord\(""\)')


def sanitize_text(s: str) -> str:
    for k, v in SANITIZE.items():
        s = s.replace(k, v)
    return s.replace("\r\n", "\n")


def fix_line(line: str) -> str:
    _orig = line
    # f"""" & print(""" openers
    line = RX_F_TRIPLE_OPEN.sub(r'\1"', line)
    line = RX_PRINT_TRIPLE_OPEN.sub(r'\1"', line)
    # collapse huge runs to triple
    line = RX_RUN_4PLUS.sub('"""', line)
    # specific bracketed keys like [""author""]
    line = RX_IDX_DBL_QUOTED.sub(r'["\1"]', line)
    # fix = ""  start
    line = RX_EQ_DBL_QUOTE_L.sub('= "', line)
    # fix end side: ""), -> "), etc.
    line = RX_DBL_QUOTE_R.sub(r'"\1', line)
    # finally, reduce any isolated "" to "
    line = RX_RUN_2.sub('"', line)
    # wrap alphabet="..." as raw triple quotes
    m = RX_ALPHABET.match(line.strip())
    if m:
        line = 'alphabet=r"""%s"""\n' % m.group(1)
    # ord("") -> ord("*") (avoid empty-char parsing)
    line = RX_ORD_EMPTY.sub('ord("*")', line)
    return line


def process_file(path: str):
    # backup
    dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    s = sanitize_text(src)

    # line-wise fix
    lines = s.splitlines(True)
    fixed = [fix_line(ln) for ln in lines]
    out = "".join(fixed)

    changed = out != src
    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)

    try:
        py_compile.compile(path, doraise=True)
        return changed, True, ""
    except Exception as e:
        return changed, False, f"{type(e).__name__}: {e}"


def main():
    if not os.path.exists(LIST):
        print("Missing compile_failures.tsv; run tools/list_compile_failures.py first.")
        return
    rows = [("Path", "Changed", "Compiles", "Notes")]
    with open(LIST, "r", encoding="utf-8") as f:
        next(f, None)
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if not p.endswith(".py") or not os.path.exists(p):
                continue
            ch, ok, err = process_file(p)
            rows.append(
                (p, "yes" if ch else "no", "yes" if ok else "no", "" if ok else err)
            )
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t").writerows(rows)
    print("Report:", OUT)
    print("Backups:", BACKUP)


if __name__ == "__main__":
    main()
