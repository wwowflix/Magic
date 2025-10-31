#!/usr/bin/env python3
import ast
import pathlib
import re

FAIL_LIST = r".\outputs\reports\_fail_paths.txt"

SMART = {"“": '"', "”": '"', "„": '"', "‟": '"', "‘": "'", "’": "'", "‚": "'", "‛": "'"}
REPL = re.compile(r"^(>>> |\.\.\. )")
CTRL = re.compile(
    r"[\x00-\x08\x0B-\x0C\x0E-\x1F]"
)  # strip ASCII controls except \t \n \r


def ast_ok(s, fn):
    try:
        ast.parse(s, filename=fn)
        return True
    except Exception:
        return False


def load_text(p: pathlib.Path) -> str:
    b = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode("utf-8", "replace")


def normalize_common(txt: str) -> str:
    txt = txt.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    txt = CTRL.sub("", txt)
    for bad, good in SMART.items():
        txt = txt.replace(bad, good)
    # Strip REPL prompts
    txt = "\n".join(REPL.sub("", ln) for ln in txt.split("\n"))
    return txt


def fix_unterminated_strings(txt: str) -> str:
    # Handle simple single-line unterminated quotes, avoid touching triple-quotes
    out = []
    for ln in txt.split("\n"):
        line = ln
        for q in ("'", '"'):
            if '"""' in line or "'''" in line:
                continue
            # odd count of q (not escaped) → add one q at EOL
            count = 0
            i = 0
            while i < len(line):
                if line[i] == "\\":
                    i += 2
                    continue
                if line[i] == q:
                    count += 1
                i += 1
            if count % 2 == 1:
                line = line + q
        out.append(line)
    return "\n".join(out)


def fix_mixed_indent(txt: str) -> str:
    # Convert leading tabs to 4 spaces; also dedent lines that look wrongly indented
    lines = txt.split("\n")
    res = []
    prev = ""
    for ln in lines:
        # convert tabs in leading whitespace only
        lead = len(ln) - len(ln.lstrip("\t "))
        head = ln[:lead].replace("\t", ")
        tail = ln[lead:]
        ln = head + tail
        # simple heuristic: if previous significant line does NOT open a block,
        # but this line starts with spaces, try remove up to 4
        prev_sig = prev.rstrip()
        opens = prev_sig.endswith((":", "\\", "(", "[", "{"))
        if not opens and ln.startswith(") and ln.lstrip() and prev_sig:
            test = ln[4:]
            if ast_ok(prev + "\n" + test + "\n", "<line>"):
                ln = test
        res.append(ln)
        if ln.strip():
            prev = ln
    out = "\n".join(res)
    if not out.endswith("\n"):
        out += "\n"
    return out


def process(p: pathlib.Path) -> bool:
    orig = load_text(p)
    if ast_ok(orig, str(p)):
        return False
    t = normalize_common(orig)
    if t != orig and ast_ok(t, str(p)):
        p.write_text(t, encoding="utf-8")
        return True
    t2 = fix_unterminated_strings(t)
    if t2 != t and ast_ok(t2, str(p)):
        p.write_text(t2, encoding="utf-8")
        return True
    t3 = fix_mixed_indent(t2)
    if t3 != t2 and ast_ok(t3, str(p)):
        p.write_text(t3, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    still = 0
    for rel in pathlib.Path(FAIL_LIST).read_text().splitlines():
        fp = pathlib.Path(rel)
        if not fp.is_file():
            continue
        if process(fp):
            fixed += 1
        else:
            still += 1
    print(f"FIX_AST_ROUND2 fixed={fixed} still={still}")


if __name__ == "__main__":
    main()
