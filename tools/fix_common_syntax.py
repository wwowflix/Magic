import csv
import io
import os
import py_compile
import re
import shutil
import time
import tokenize

ROOT = r"D:\MAGIC"
OUT_DIR = os.path.join(ROOT, "outputs", "fix_common_syntax")
BACKUP_DIR = os.path.join(
    ROOT, "backups", f"fix_common_syntax_{time.strftime('%Y%m%d_%H%M%S')}"
)
REPORT = os.path.join(OUT_DIR, "report.tsv")
WIRE = os.path.join(ROOT, "outputs", "wire_joiner", "wire_joiner_report.tsv")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)


def normalize_text(t: str) -> str:
    return (
        t.replace("\ufeff", "")
        .replace("Â»", "")
        .replace("Â«", "")
        .replace("\u00a0", " ")
        .replace("\r\n", "\n")
        .replace("â€œ", '"')
        .replace("â€", '"')
        .replace("â€˜", "'")
        .replace("â€™", "'")
        .replace("Ã°Å¸", "")
        .replace("Ã¢â‚¬â„¢", "'")
        .replace("Ã¢â‚¬Å“", '"')
        .replace("Ã¢â‚¬ï¿½", '"')
        .replace("Ã¢â‚¬â€œ", "-")
        .replace("Ã¢â‚¬â€", "-")
        .replace("Ã‚", "")
    )


REPLACERS = [
    (re.compile(r"(?m)^\s*print\s+'([^']*)'\s*$"), r'print("\1")'),
    (re.compile(r'(?m)^\s*print\s+"([^"]*)"\s*$'), r'print("\1")'),
    (re.compile(r"(?m)^\s*print\s+([^\(\n][^\n]*)$"), r"print(\1)"),
    (
        re.compile(r"(?m)except\s+([A-Za-z_][\w\.]*)\s*,\s*([A-Za-z_]\w*)\s*:"),
        r"except \1 as \2:",
    ),
    (re.compile(r"<>"), r"!="),
    (re.compile(r"\bxrange\b"), r"range"),
    (re.compile(r"\braw_input\b"), r"input"),
]


def read_wire_joiner_failures():
    paths = []
    if not os.path.exists(WIRE):
        return paths
    with open(WIRE, "r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            issue, path = parts[0], parts[1]
            if (
                issue == "COMPILE_FAIL"
                and path.endswith(".py")
                and os.path.exists(path)
            ):
                paths.append(path)
    return sorted(set(paths))


def try_compile(path):
    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# FAST placeholder detector (no heavy regex)
def is_tiny_or_placeholder(txt: str) -> bool:
    s = txt.strip()
    if len(s) <= 200:
        return True
    # avoid huge files
    if len(s) > 200_000:
        return False
    # docstring-only quick check
    if (s.startswith('"""') and s.endswith('"""')) or (
        s.startswith("'''") and s.endswith("'''")
    ):
        # if the interior has very little code-like content, treat as placeholder
        inner = s[3:-3].strip()
        if len(inner) <= 200 and not any(ch in inner for ch in ":(){}[]=;"):
            return True
    # token-based: only comments/strings/whitespace
    try:
        code_tokens = []
        for tok in tokenize.generate_tokens(io.StringIO(txt).readline):
            if tok.type in (
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.INDENT,
                tokenize.DEDENT,
            ):
                continue
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            code_tokens.append(tok)
        return len(code_tokens) == 0
    except Exception:
        return False


def process_file(path, rows):
    rel = os.path.relpath(path, ROOT)
    dst = os.path.join(BACKUP_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        original = f.read()
    text = normalize_text(original)

    changed = False
    for rx, rep in REPLACERS:
        new_text = rx.sub(rep, text)
        if new_text != text:
            changed = True
            text = new_text

    if changed or text != original:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    ok, err = try_compile(path)
    if ok:
        rows.append(["FIXED", path, "OK after edits", ""])
        return

    if is_tiny_or_placeholder(text):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("# auto-stubbed by fix_common_syntax\npass\n")
        ok2, err2 = try_compile(path)
        if ok2:
            rows.append(["STUBBED", path, "Replaced with pass", "tiny/placeholder"])
            return

    rows.append(["STILL_FAIL", path, "Manual review", err])


def main():
    failing = read_wire_joiner_failures()
    if not failing:
        print("No COMPILE_FAIL files found in wire_joiner_report.tsv; nothing to do.")
        return
    rows = []
    for i, p in enumerate(failing, 1):
        try:
            process_file(p, rows)
        except Exception as e:
            rows.append(["ERROR", p, "Exception", str(e)])
        if i % 25 == 0:
            print(f"...processed {i}/{len(failing)}")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["Result", "Path", "Action", "Notes"])
        w.writerows(rows)

    from collections import Counter

    c = Counter(r[0] for r in rows)
    print("Summary:", dict(c))
    print("Report:", REPORT)
    print("Backups:", BACKUP_DIR)


if __name__ == "__main__":
    main()
