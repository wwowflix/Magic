import os, re, time, shutil, py_compile, pathlib

ROOT = r"D:\MAGIC"
FAIL_TSV = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(
    ROOT, "backups", f"stepB_docstrings_{time.strftime('%Y%m%d_%H%M%S')}"
)
os.makedirs(BACKUP, exist_ok=True)

# ----- regexes
RX_SIX_QUOTES_LINE = re.compile(r'""""""')
RX_BROKEN_EMPTY_WITH_BSLASH = re.compile(r'^(?P<prefix>\s*\w[\w\.]*\s*=\s*)""\s*\\\s*$')
RX_TOP_PROSE = re.compile(
    r'^[A-Za-z0-9 _\-\(\)\[\],.:;`\'"]/'
)  # first non-comment line looks like prose
RX_SCM_DATE = re.compile(r"^\s*\$Date:.*$\Z", re.M)
RX_NAKED_DEF = re.compile(r"^(\s*)(def|class)\s+\w[^\n]*:\s*$", re.M)
RX_NAKED_WITH_TRY = re.compile(r"^(\s*)(with|try)\b[^\n]*:\s*$", re.M)
RX_DANGLING_TRIPLE = re.compile(r'^\s*(?:r?""")\s*$')
RX_WARNMSG = re.compile(r'^(\s*_warnmsg\s*=\s*")([^"]*)$')  # opens but never closes
RX_AUTO_DF = re.compile(
    r'auto_df\[""author""\]\s*=\s*auto_df\.get\(""\s*author\s*"",\s*""\)'
)


def compiles(p: str) -> bool:
    try:
        py_compile.compile(p, doraise=True)
        return True
    except Exception:
        return False


def wrap_top_prose(text: str) -> str:
    # If the very first significant line is prose (not # / """ / import / from), wrap until first blank line
    lines = text.splitlines(True)
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        return text
    first = lines[i].lstrip()
    if first.startswith(("#", "'''", '"""', "from ", "import ")):
        return text
    if RX_TOP_PROSE.match(first):
        j = i
        while j < len(lines) and lines[j].strip() != "":
            j += 1
        block = "".join(lines[i:j])
        new = lines[:i] + ['"""\\n', block, '\\n"""\\n'] + lines[j:]
        return "".join(new)
    return text


def normalize_quotes_and_blocks(text: str) -> str:
    lines = text.splitlines(True)
    out, i, n = [], 0, len(lines)
    while i < n:
        line = RX_SIX_QUOTES_LINE.sub('"""', lines[i])

        m = RX_BROKEN_EMPTY_WITH_BSLASH.match(line)
        if m:
            # turn   foo = ""\   + continuation lines  ->  foo = r""" ... """
            prefix = m.group("prefix")
            body = []
            i += 1
            while i < n:
                cur = RX_SIX_QUOTES_LINE.sub('"""', lines[i])
                if cur.rstrip().endswith("\\"):
                    body.append(cur.rstrip()[:-1] + "\n")
                    i += 1
                else:
                    body.append(cur if cur.endswith("\n") else cur + "\n")
                    break
            out.append(f'{prefix}r"""\n')
            out.extend(body)
            out.append('"""\n')
            i += 1
            continue

        # collapse a lone dangling triple quote into empty docstring
        if RX_DANGLING_TRIPLE.match(line):
            out.append('"""\\n"""\n')
            i += 1
            continue

        out.append(line)
        i += 1

    txt = "".join(out)

    # comment out $Date: ... lines
    txt = RX_SCM_DATE.sub(lambda m: "# " + m.group(0).lstrip(), txt)

    # ensure bodies where they went missing
    txt = RX_NAKED_DEF.sub(
        lambda m: m.group(1) + m.group(0).strip() + "\n" + m.group(1) + "    pass\n",
        txt,
    )
    txt = RX_NAKED_WITH_TRY.sub(
        lambda m: m.group(1) + m.group(0).strip() + "\n" + m.group(1) + "    pass\n",
        txt,
    )

    # close obvious _warnmsg openers into a triple-quoted block (yacc)
    def _fix_warn(s: re.Match) -> str:
        indent, head = s.group(1), s.group(2)
        return f'{indent}"""PLY: {head}\\n"""\n'

    txt = RX_WARNMSG.sub(_fix_warn, txt)

    # normalize the author get() which may have doubled quotes during prior passes
    txt = RX_AUTO_DF.sub('auto_df["author"] = auto_df.get("author", "")', txt)

    return txt


def process(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        orig = f.read()
    text = wrap_top_prose(orig)
    text = normalize_quotes_and_blocks(text)
    changed = text != orig
    if changed:
        dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return changed


def main():
    if not os.path.exists(FAIL_TSV):
        print("Missing compile_failures.tsv; run tools/list_compile_failures.py first.")
        return
    paths = []
    with open(FAIL_TSV, "r", encoding="utf-8") as f:
        next(f, None)
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if p.endswith(".py") and os.path.exists(p):
                paths.append(p)

    changed = compiled = 0
    for p in paths:
        did = process(p)
        if did:
            changed += 1
        if compiles(p):
            compiled += 1

    print(f"Files touched: {changed} / {len(paths)} | now compiling: {compiled}")
    print("Backups:", BACKUP)


if __name__ == "__main__":
    main()
