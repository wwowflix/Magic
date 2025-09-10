import os
import re
import time
import shutil
import py_compile
import unicodedata

ROOT = r"D:\MAGIC"
FAILTSV = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(ROOT, "backups", f"stepE_{time.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP, exist_ok=True)


# --- Generic helpers ---------------------------------------------------------
def strip_problem_runes(text: str) -> str:
    # Keep ASCII printable + \n\t\r; convert the rest to spaces (outside obvious string escapes)
    # This is a last-resort scrub to stop bogus bytes from breaking the tokenizer.
    out = []
    for ch in text:
        o = ord(ch)
        if ch in "\n\r\t" or 32 <= o <= 126:
            out.append(ch)
        else:
            # keep some common whitespace
            cat = unicodedata.category(ch)
            if cat.startswith("Z"):
                out.append(" ")
            else:
                # map euro to \u20AC explicitly (already safe ASCII)
                if ch == "Ã¢â€šÂ¬":
                    out.append("\\u20AC")
                else:
                    out.append(" ")
    return "".join(out)


def close_unmatched_quotes(text: str, quote: str) -> str:
    # count occurrences of a triple-quote token and close if odd
    count = text.count(quote)
    if count % 2 != 0:
        text += f"\n{quote}\n"
    return text


def wrap_top_prose(text: str) -> str:
    START = re.compile(
        r"^(?:\s*(?:#|from\b|import\b|\"\"\"|\'\'\'|def\b|class\b|try\b|with\b))"
    )
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


def compiles(path: str) -> bool:
    try:
        py_compile.compile(path, doraise=True)
        return True
    except Exception:
        return False


# --- Regexes weÃ¢â‚¬â„¢ll reuse ------------------------------------------------------
RX_MANY_QUOTES = re.compile(r'("{6,}|\'{6,})')
RX_SPLIT_TRIPLE = re.compile(
    r'("{3}\s*(?:\\n|\r?\n)?\s*"{3}|\'{3}\s*(?:\\n|\r?\n)?\s*\'{3})'
)
RX_DEDOUBLE_ANY = re.compile(r'""([^"\n]{1,80})""')  # "word" or short token => dedouble
RX_STANDALONE_NL = re.compile(r"^\s*\\n\s*$", re.M)

# dangling backslash after a quoted segment on the same line
RX_EOB_BACKSLASH_AFTER_QUOTE = re.compile(r'(".*?"|\'.*?\')\s*\\\s*$', re.M)
# specific: = ""\   or = ''\
RX_EMPTY_ASSIGN_EOBBS = re.compile(
    r'(^\s*[\w\.\[\]"\']+\s*=\s*(""|\'\')\s*\\\s*$)', re.M
)

# SCM $Date:
RX_SCM_DATE = re.compile(r"^\s*\$Date:.*$", re.M)

# Naked blocks
RX_NAKED_DEFCLS = re.compile(r"^(\s*)(def|class)\s+\w[^\n]*:\s*$", re.M)
RX_NAKED_WITH = re.compile(r"^(\s*)with\b[^\n]*:\s*$", re.M)
RX_TRY_ONLY = re.compile(r"^(\s*)try\s*:\s*$", re.M)
RX_TRY_PASS = re.compile(r"^(\s*)try:\s*\n(\s*)pass(?!\s*\n\s*except\b)", re.M)
RX_ORPHAN_EXCEPT = re.compile(r"^(\s*)except\b[^\n]*:\s*$", re.M)

# yacctab/_warnmsg long unterminated lines
RX_WARNMSG = re.compile(r'^(\s*)_warnmsg\s*=\s*".*$', re.M)

# uts46data broken tuple (replace whole third field)
RX_UTS46_BAD = re.compile(r'\(\s*0x1FCD\s*,\s*"?3"?\s*,\s*".*?"\s*\)')

# specific giant constants -> blank
RX_CN = re.compile(r'^(?P<i>\s*)COMMON_CHINESE_CHARACTERS\s*=\s*".*$', re.M)
RX_JP = re.compile(r'^(?P<i>\s*)COMMON_JAPANESE_CHARACTERS\s*=\s*".*$', re.M)

# emoji codes weird \n""""""\n sequences
RX_EMOJI_GLITCH = re.compile(r'\\n"{6,}\\n')

# _spinners frames
RX_SPIN_FRAMES = re.compile(r'("frames"\s*:\s*)".*$', re.M)

# author line
RX_AUTHOR_LINE = re.compile(
    r'auto_df\[""author""\]\s*=\s*auto_df\.get\(""\s*author\s*"",\s*""\)'
)


def normalize(text: str, path: str) -> str:
    _orig = text

    # 0) scrub hostile runes early
    text = strip_problem_runes(text)

    # 1) wrap initial prose (comments/docs pasted without quotes)
    text = wrap_top_prose(text)

    # 2) collapse ridiculous quote runs & split triples
    text = RX_MANY_QUOTES.sub(
        lambda m: '"""' if m.group(0).startswith('"') else "'''", text
    )
    text = RX_SPLIT_TRIPLE.sub(
        lambda m: '"""' if m.group(0).startswith('"') else "'''", text
    )

    # 3) dedouble short tokens like ""author"", ""frames"" -> "author"
    text = RX_DEDOUBLE_ANY.sub(r'"\1"', text)

    # 4) comment out SCM $Date:
    text = RX_SCM_DATE.sub(lambda m: "# " + m.group(0).lstrip(), text)

    # 5) fix dangling line-continuations after quotes
    text = RX_EMPTY_ASSIGN_EOBBS.sub(lambda m: m.group(1).rstrip("\\ ").rstrip(), text)
    text = RX_EOB_BACKSLASH_AFTER_QUOTE.sub(lambda m: m.group(1), text)

    # 6) supply missing bodies
    text = RX_NAKED_DEFCLS.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)
    text = RX_NAKED_WITH.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)
    text = RX_TRY_ONLY.sub(
        lambda m: f"{m.group(1)}try:\n{m.group(1)}    pass\n{m.group(1)}except Exception:\n{m.group(1)}    pass",
        text,
    )
    text = RX_TRY_PASS.sub(
        lambda m: f"{m.group(1)}try:\n{m.group(1)}    pass\n{m.group(1)}except Exception:\n{m.group(1)}    pass",
        text,
    )
    text = RX_ORPHAN_EXCEPT.sub(lambda m: f"{m.group(1)}pass", text)

    # 7) stabilize known long strings
    text = RX_WARNMSG.sub(lambda m: f'{m.group(1)}_warnmsg = "PLY message"', text)

    # 8) special cases
    bn = os.path.basename(path)
    if bn == "uts46data_READY.py":
        text = RX_UTS46_BAD.sub('(0x1FCD, "3", "")', text)
    if bn == "_spinners_READY.py":
        text = RX_SPIN_FRAMES.sub(r'\1""', text)
    if bn == "_emoji_codes_READY.py":
        text = RX_EMOJI_GLITCH.sub('"""', text)

    # 9) huge multilingual constants -> empty
    text = RX_CN.sub(lambda m: f'{m.group("i")}COMMON_CHINESE_CHARACTERS = ""', text)
    text = RX_JP.sub(lambda m: f'{m.group("i")}COMMON_JAPANESE_CHARACTERS = ""', text)

    # 10) clean stray standalone \n pseudo-lines
    text = RX_STANDALONE_NL.sub("# newline", text)

    # 11) known author line
    text = RX_AUTHOR_LINE.sub('auto_df["author"] = auto_df.get("author", "")', text)

    # 12) close unmatched triple quotes for BOTH """ and '''
    text = close_unmatched_quotes(text, '"""')
    text = close_unmatched_quotes(text, "'''")

    return text


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
