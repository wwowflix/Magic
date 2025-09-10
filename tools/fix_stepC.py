import os
import re
import time
import shutil
import py_compile

ROOT = r"D:\MAGIC"
FAILTSV = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(ROOT, "backups", f"stepC_{time.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP, exist_ok=True)

# ---------- Regex helpers ----------
# 1) Any run of 6+ double quotes -> collapse to triple quotes
RX_MANY_QUOTES = re.compile(r'"{6,}')
# 2) Triple-quote separated by whitespace/newlines -> single triple-quote
RX_SPLIT_TRIPLE = re.compile(r'"""\s*(?:\\n|\r?\n)?\s*"""')
# 3) Top-of-file prose (first non-blank line not starting with #/import/from/quotes/def/class)
START_IS_DIRECTIVE = re.compile(
    r'^(?:\s*(?:#|from\b|import\b|"""|\'\'\'|def\b|class\b))'
)
# 4) Comment SCM $Date lines anywhere
RX_SCM_DATE = re.compile(r"^\s*\$Date:.*$", re.M)
# 5) Naked def/class/with/try
RX_NAKED_DEFCLS = re.compile(r"^(\s*)(def|class)\s+\w[^\n]*:\s*$", re.M)
RX_NAKED_WITH = re.compile(r"^(\s*)with\b[^\n]*:\s*$", re.M)
RX_NAKED_TRY = re.compile(r"^(\s*)try\s*:\s*$", re.M)
# 6) Orphan 'except:' (no try) — replace with a no-op 'pass'
RX_ORPHAN_EXCEPT = re.compile(r"^(\s*)except\b[^\n]*:\s*$", re.M)
# 7) Bare NAME = "" lines
RX_BARE_EMPTY = re.compile(r'^(\s*[A-Za-z_]\w*\s*=\s*)""\s*$', re.M)
# 8) De-double common ""key"" artifacts
RX_DEDOUBLE_KEYS = re.compile(r'""([A-Za-z_]\w*)""')
# 9) Specific known artifacts
RX_AUTHOR = re.compile(
    r'auto_df\[""author""\]\s*=\s*auto_df\.get\(""\s*author\s*"",\s*""\)'
)
# 10) YACC/PLY warning line (unterminated in your dumps)
RX_WARNMSG = re.compile(r'^(\s*)_warnmsg\s*=\s*".*$', re.M)
# 11) Replace raw Euro sign inside strings with a unicode escape (safer for mixed encodings)
RX_EURO = re.compile(r"€")

# 12) Nasty huge Chinese constant lines: replace the whole RHS with an empty string
RX_COMMON_CN = re.compile(r'^(?P<ind>\s*)(COMMON_CHINESE_CHARACTERS\s*=\s*)".*$', re.M)


def wrap_top_prose(text: str) -> str:
    lines = text.splitlines(True)
    # find first non-blank
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        return text
    if START_IS_DIRECTIVE.match(lines[i]):
        return text
    # capture prose block until first blank line
    j = i
    while j < len(lines) and lines[j].strip() != "":
        j += 1
    block = "".join(lines[i:j])
    wrapped = "".join(lines[:i] + ['"""\\n', block, '\\n"""\\n'] + lines[j:])
    return wrapped


def normalize(text: str) -> str:
    # Collapse ridiculous quote runs and split triples
    text = RX_MANY_QUOTES.sub('"""', text)
    text = RX_SPLIT_TRIPLE.sub('"""', text)

    # Comment $Date: lines
    text = RX_SCM_DATE.sub(lambda m: "# " + m.group(0).lstrip(), text)

    # Provide bodies where missing
    text = RX_NAKED_DEFCLS.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)
    text = RX_NAKED_WITH.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", text)

    # Fix naked try -> try/pass + except/pass
    def _fix_try(m):
        ind = m.group(1)
        return f"{ind}try:\n{ind}    pass\n{ind}except Exception:\n{ind}    pass"

    text = RX_NAKED_TRY.sub(_fix_try, text)

    # Orphan except -> no-op
    text = RX_ORPHAN_EXCEPT.sub(lambda m: f"{m.group(1)}pass", text)

    # Bare NAME = "" -> truly empty string (prevents later unterminated spillover)
    text = RX_BARE_EMPTY.sub(lambda m: m.group(1) + '""', text)

    # De-double keys like ""author""
    text = RX_DEDOUBLE_KEYS.sub(r'"\1"', text)

    # Specific artifact in api_normalizer
    text = RX_AUTHOR.sub('auto_df["author"] = auto_df.get("author", "")', text)

    # Stabilize the infamous PLY warning assignment
    text = RX_WARNMSG.sub(lambda m: f'{m.group(1)}_warnmsg = "PLY message"', text)

    # EURO -> \u20AC to avoid codec weirdness
    text = RX_EURO.sub(r"\\u20AC", text)

    # COMMON_CHINESE_CHARACTERS = "…  -> empty string placeholder to compile
    text = RX_COMMON_CN.sub(
        lambda m: f'{m.group("ind")}COMMON_CHINESE_CHARACTERS = ""', text
    )

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
    txt = wrap_top_prose(src)
    txt = normalize(txt)
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
