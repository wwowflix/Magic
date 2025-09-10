import os, re, time, shutil, py_compile, io

ROOT = r"D:\MAGIC"
FAILTSV = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(ROOT, "backups", f"stepD_{time.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP, exist_ok=True)

# ---------- Patterns ----------
RX_MANY_QUOTES = re.compile(r'"{6,}')
RX_SPLIT_TRIPLE = re.compile(r'"""\s*(?:\\n|\r?\n)?\s*"""')
RX_DEDOUBLE_KEYS = re.compile(r'""([A-Za-z_]\w*)""')
RX_BARE_EMPTY = re.compile(r'^(\s*[A-Za-z_]\w*\s*=\s*)""\s*$', re.M)

# trailing backslash right after opening empty string: foo = ""\
RX_EQ_EMPTY_BS = re.compile(
    r'(^\s*[\w\.\[\]"\']+\s*=\s*""\)\\\s*$|^\s*[\w\.\[\]"\']+\s*=\s*""\\\s*$)', re.M
)
RX_EQ_EMPTY_BS2 = re.compile(r'(^\s*[\w\.\[\]"\']+\s*=\s*\'\'\\\s*$)', re.M)

# any "... \  " before immediate quotes on next line -> drop the backslash
RX_JOINED_BS = re.compile(r'\\\s*(\n\s*""")')

# comment SCM $Date:
RX_SCM_DATE = re.compile(r"^\s*\$Date:.*$", re.M)

# naked def/class/with
RX_NAKED_DEFCLS = re.compile(r"^(\s*)(def|class)\s+\w[^\n]*:\s*$", re.M)
RX_NAKED_WITH = re.compile(r"^(\s*)with\b[^\n]*:\s*$", re.M)

# "try:" that has only pass and no except -> add except
RX_TRY_PASS = re.compile(r"^(\s*)try:\s*\n(\s*)pass(?!\s*\n\s*except\b)", re.M)
# completely naked try:
RX_NAKED_TRY = re.compile(r"^(\s*)try\s*:\s*$", re.M)
# orphan except:
RX_ORPHAN_EXCEPT = re.compile(r"^(\s*)except\b[^\n]*:\s*$", re.M)

# unlucky warnmsg (unterminated in dumps)
RX_WARNMSG = re.compile(r'^(\s*)_warnmsg\s*=\s*".*$', re.M)

# euro sign -> escape
RX_EURO = re.compile(r"€")

# specific giant constants -> blank them
RX_CN = re.compile(r'^(?P<i>\s*)COMMON_CHINESE_CHARACTERS\s*=\s*".*$', re.M)
RX_JP = re.compile(r'^(?P<i>\s*)COMMON_JAPANESE_CHARACTERS\s*=\s*".*$', re.M)

# bad lines like: \n on its own (outside a string)
RX_STANDALONE_NL = re.compile(r"^\s*\\n\s*$", re.M)

# _spinners: frames payload → empty string (garbled runes)
RX_SPIN_FRAMES = re.compile(r'("frames"\s*:\s*)".*$', re.M)

# uts46data broken tuple with euro/garble -> replace whole field to a clean empty string
RX_UTS46_BAD = re.compile(r'\(\s*0x1FCD\s*,\s*"?3"?\s*,\s*".*?"\s*\)')

# de-double “author” keys specifically
RX_AUTHOR_LINE = re.compile(
    r'auto_df\[""author""\]\s*=\s*auto_df\.get\(""\s*author\s*"",\s*""\)'
)


def close_unmatched_triple_quotes(text: str) -> str:
    count = text.count('"""')
    if count % 2 != 0:
        # Append a closing triple quote on its own line
        text += '\n"""\n'
    return text


def wrap_top_prose(text: str) -> str:
    START = re.compile(r'^(?:\s*(?:#|from\b|import\b|"""|\'\'\'|def\b|class\b|try\b))')
    lines = text.splitlines(True)
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        return text
    if START.match(lines[i]):
        return text
    j = i
    while j < len(lines) and lines[j].strip() != "":
        j += 1
    block = "".join(lines[i:j])
    return "".join(lines[:i] + ['"""\\n', block, '\\n"""\\n'] + lines[j:])


def normalize(text: str, path: str) -> str:
    orig = text

    # 0) wrap top prose
    text = wrap_top_prose(text)

    # 1) quote normalizations
    text = RX_MANY_QUOTES.sub('"""', text)
    text = RX_SPLIT_TRIPLE.sub('"""', text)

    # 2) simple key fixes, empties
    text = RX_DEDOUBLE_KEYS.sub(r'"\1"', text)
    text = RX_BARE_EMPTY.sub(lambda m: m.group(1) + '""', text)

    # 3) remove trailing line-continuation backslashes after empty string assignments
    text = RX_EQ_EMPTY_BS.sub(lambda m: m.group(0).rstrip("\\").rstrip(), text)
    text = RX_EQ_EMPTY_BS2.sub(lambda m: m.group(0).rstrip("\\").rstrip(), text)
    text = RX_JOINED_BS.sub(r"\1", text)

    # 4) comment $Date:
    text = RX_SCM_DATE.sub(lambda m: "# " + m.group(0).lstrip(), text)

    # 5) supply bodies where missing
    text = RX_NAKED_DEFCLS.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)
    text = RX_NAKED_WITH.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)

    # 6) try/except healing
    text = RX_NAKED_TRY.sub(
        lambda m: f"{m.group(1)}try:\n{m.group(1)}    pass\n{m.group(1)}except Exception:\n{m.group(1)}    pass",
        text,
    )
    text = RX_TRY_PASS.sub(
        lambda m: f"{m.group(1)}try:\n{m.group(1)}    pass\n{m.group(1)}except Exception:\n{m.group(1)}    pass",
        text,
    )
    text = RX_ORPHAN_EXCEPT.sub(lambda m: f"{m.group(1)}pass", text)

    # 7) stabilize warnmsg
    text = RX_WARNMSG.sub(lambda m: f'{m.group(1)}_warnmsg = "PLY message"', text)

    # 8) escape euros
    text = RX_EURO.sub("\\u20AC", text)

    # 9) nuke giant constants
    text = RX_CN.sub(lambda m: f'{m.group("i")}COMMON_CHINESE_CHARACTERS = ""', text)
    text = RX_JP.sub(lambda m: f'{m.group("i")}COMMON_JAPANESE_CHARACTERS = ""', text)

    # 10) remove stray standalone \n lines
    text = RX_STANDALONE_NL.sub("# newline", text)

    # 11) file-specific sanitizers
    bn = os.path.basename(path)
    if bn == "_spinners_READY.py":
        text = RX_SPIN_FRAMES.sub(r'\1""', text)
    if bn == "_emoji_codes_READY.py":
        # normalize any lingering weird quote runs again
        text = RX_MANY_QUOTES.sub('"""', text)
        text = RX_SPLIT_TRIPLE.sub('"""', text)
        text = RX_STANDALONE_NL.sub("# newline", text)
    if bn == "uts46data_READY.py":
        text = RX_UTS46_BAD.sub('(0x1FCD, "3", "")', text)

    # 12) specific author line
    text = RX_AUTHOR_LINE.sub('auto_df["author"] = auto_df.get("author", "")', text)

    # 13) close unmatched triple quotes at EOF
    text = close_unmatched_triple_quotes(text)

    return text


def compiles(path: str) -> bool:
    try:
        py_compile.compile(path, doraise=True)
        return True
    except Exception:
        return False


def process(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    txt = normalize(src, path)
    if txt != src:
        dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        return True
    return False


def main():
    if not os.path.exists(FAILTSV):
        print("Missing compile_failures.tsv")
        return
    paths = []
    with open(FAILTSV, "r", encoding="utf-8") as f:
        next(f, None)
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if p.endswith(".py") and os.path.exists(p):
                paths.append(p)

    touched = ok = 0
    for p in paths:
        if process(p):
            touched += 1
        if compiles(p):
            ok += 1
    print(f"Touched {touched}/{len(paths)} | Now compiling: {ok}")
    print("Backup:", BACKUP)


if __name__ == "__main__":
    main()
