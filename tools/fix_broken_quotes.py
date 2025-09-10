import os, re, io, sys, csv, time, shutil, py_compile, pathlib

ROOT = r"D:\MAGIC"
LIST = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(
    ROOT, "backups", f"fix_broken_quotes_{time.strftime("%Y%m%d_%H%M%S")}"
)
OUT = os.path.join(ROOT, "outputs", "reports", "fix_broken_quotes_report.tsv")
os.makedirs(BACKUP, exist_ok=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Remove/control/sanitize common trouble chars (most already covered in wire_joiner;
# keep here so this fixer is self-contained on just the failing files).
SANITIZE_MAP = {
    **{chr(c): "" for c in range(0x80, 0xA0)},  # U+0080..U+009F -> remove
    "\ufeff": "",
    "Â": "",
    "ðŸ": "",
    "â€™": "'",
    "â€œ": '"',
    "â€�": '"',
    "â€“": "-",
    "â€”": "-",
}


def sanitize_text(s: str) -> str:
    for k, v in SANITIZE_MAP.items():
        s = s.replace(k, v)
    # Normalize Windows CRLF to LF
    s = s.replace("\r\n", "\n")
    return s


# Heuristics to collapse bad quote runs safely.
# Order matters: handle docstrings first (4+ quotes -> 3), then generic doubles -> single.
RX_F_TRIPLE_OPEN = re.compile(r'(\bf)\s*"""+')  # f"""" -> f"
RX_PRINT_TRIPLE_OPEN = re.compile(r'(\bprint\s*\()\s*"""+')  # print(""" -> print("
RX_RUN_4PLUS = re.compile(r'"{4,}')  # "..." with >= 4 quotes
RX_RUN_2 = re.compile(r'(?<!")""(?!")')  # exactly two quotes not part of triple/run
RX_ALPHABET = re.compile(r'^\s*alphabet\s*=\s*"(.*)"\s*,?\s*$', re.UNICODE)


def fix_quoting(text: str) -> str:
    out_lines = []
    for line in text.splitlines(True):
        orig = line
        # quick skips: leave proper triple-quoted docstrings alone
        # but if we see f"""" or print(""" patterns, collapse to a single opener
        line = RX_F_TRIPLE_OPEN.sub(r'\1"', line)
        line = RX_PRINT_TRIPLE_OPEN.sub(r'\1"', line)

        # collapse 4+ quotes to triple (docstrings)
        line = RX_RUN_4PLUS.sub('"""', line)

        # collapse stray double-quotes to single "
        line = RX_RUN_2.sub('"', line)

        # special case: alphabet="..." -> alphabet=r"""..."""
        m = RX_ALPHABET.match(line.strip())
        if m:
            inner = m.group(1)
            # keep as-is but guard with raw triple quotes so quotes/Unicode don't break parsing
            line = re.sub(RX_ALPHABET, 'alphabet=r"""\\1"""', line.rstrip("\n")) + "\n"

        out_lines.append(line)
    return "".join(out_lines)


def try_compile(path):
    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def process(path: str):
    # backup original
    dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    s1 = sanitize_text(src)
    s2 = fix_quoting(s1)

    changed = s2 != src
    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(s2)

    ok, err = try_compile(path)
    return changed, ok, err


def main():
    if not os.path.exists(LIST):
        print("Missing compile_failures.tsv; run tools/list_compile_failures.py first.")
        sys.exit(0)

    rows = [("Path", "Changed", "Compiles", "Notes")]
    with open(LIST, "r", encoding="utf-8") as f:
        next(f, None)  # header
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if not p or not p.endswith(".py") or not os.path.exists(p):
                continue
            changed, ok, err = process(p)
            rows.append(
                (
                    p,
                    "yes" if changed else "no",
                    "yes" if ok else "no",
                    "" if ok else err,
                )
            )

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerows(rows)

    # tiny summary
    fixed = sum(1 for r in rows[1:] if r[2] == "yes")
    print(f"Wrote {OUT}. Compiling now OK: {fixed}/{len(rows)-1}")
    print(f"Backups in {BACKUP}")


if __name__ == "__main__":
    main()
