import os
import re
import time
import shutil
import py_compile

ROOT = r"D:\MAGIC"
FAIL = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(ROOT, "backups", f"stepB_plus_{time.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP, exist_ok=True)

# ---- regexes
RX_SIX_QUOTES_ANY = re.compile(
    r'""""""(?:\\n)?"""""?"'
)  # collapse 6 quotes (with/without \n) to """
RX_TOP_PROSE_LINE = re.compile(r"[A-Za-z0-9_].*")  # looks like plain text
RX_SCM_DATE_ANY = re.compile(r"^\s*\$Date:.*$", re.M)

RX_NAKED_DEFCLS = re.compile(r"^(\s*)(def|class)\s+\w[^\n]*:\s*$", re.M)
RX_NAKED_WITH = re.compile(r"^(\s*)with\b[^\n]*:\s*$", re.M)
RX_NAKED_TRY = re.compile(r"^(\s*)try\s*:\s*$", re.M)

# assignments that were intended to be multi-line but became bare: NAME = ""  (on its own line)
RX_BARE_EMPTY_EQ = re.compile(r'^(\s*[A-Za-z_]\w*\s*=\s*)""\s*$', re.M)

# common doubled-quote artifact
RX_AUTHOR = re.compile(
    r'auto_df\[""author""\]\s*=\s*auto_df\.get\(""\s*author\s*"",\s*""\)'
)


def wrap_top_prose(txt: str) -> str:
    lines = txt.splitlines(True)
    i = 0
    # skip initial blanks and encoding comments
    while i < len(lines) and (
        lines[i].strip() == ""
        or lines[i].lstrip().startswith(("#", "from ", "import ", '"""', "'''"))
        is False
        and False
    ):
        break
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        return txt
    first = lines[i]
    # if already starts with comment/import/quotes, leave it
    if first.lstrip().startswith(("#", '"""', "'''", "from ", "import ")):
        return txt
    if RX_TOP_PROSE_LINE.match(first.lstrip()):
        j = i
        while j < len(lines) and lines[j].strip() != "":
            j += 1
        block = "".join(lines[i:j])
        return "".join(lines[:i] + ['"""\\n', block, '\\n"""\\n'] + lines[j:])
    return txt


def normalize(txt: str) -> str:
    # 1) collapse broken six-quote constructs
    txt = RX_SIX_QUOTES_ANY.sub('"""', txt)

    # 2) comment $Date headers anywhere
    txt = RX_SCM_DATE_ANY.sub(lambda m: "# " + m.group(0).lstrip(), txt)

    # 3) give bodies where they went missing
    txt = RX_NAKED_DEFCLS.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", txt)
    txt = RX_NAKED_WITH.sub(lambda m: f"{m.group(0)}\n{m.group(1)}    pass", txt)

    # 4) fix naked try: add body *and* except
    def _fix_try(m):
        ind = m.group(1)
        return f"{ind}try:\n{ind}    pass\n{ind}except Exception:\n{ind}    pass"

    txt = RX_NAKED_TRY.sub(_fix_try, txt)

    # 5) bare NAME = "" lines -> explicitly empty (prevents “unterminated string” when later text confused parser)
    txt = RX_BARE_EMPTY_EQ.sub(lambda m: m.group(1) + '""', txt)

    # 6) specific artifact in api_normalizer
    txt = RX_AUTHOR.sub('auto_df["author"] = auto_df.get("author", "")', txt)

    return txt


def compiles(path: str) -> bool:
    try:
        py_compile.compile(path, doraise=True)
        return True
    except Exception:
        return False


def process(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        orig = f.read()
    txt = wrap_top_prose(orig)
    txt = normalize(txt)
    if txt != orig:
        dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        return True
    return False


def main():
    if not os.path.exists(FAIL):
        print("Missing compile_failures.tsv")
        return
    paths = []
    with open(FAIL, "r", encoding="utf-8") as f:
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
