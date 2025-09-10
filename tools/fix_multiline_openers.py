import os
import re
import time
import shutil
import py_compile

ROOT = r"D:\MAGIC"
LIST = os.path.join(ROOT, "outputs", "reports", "compile_failures.tsv")
BACKUP = os.path.join(
    ROOT, "backups", f"fix_multiline_openers_{time.strftime('%Y%m%d_%H%M%S')}"
)
os.makedirs(BACKUP, exist_ok=True)

# patterns
RX_EQ_EMPTY_BACKSLASH = re.compile(
    r'^(?P<prefix>\s*\w[\w\.]*\s*=\s*)""\s*\\\s*$'
)  # foo = ""\  (line-continue)
RX_SIX_QUOTES = re.compile(r'""""""')  # collapse 6 quotes -> 3
RX_TRIPLE_OPEN_AT_END = re.compile(r'^\s*(r?""")\s*$')  # bare triple quote line


def compiles(path: str) -> bool:
    try:
        py_compile.compile(path, doraise=True)
        return True
    except Exception:
        return False


def fix_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines(True)

    changed = False
    out = []
    i = 0
    N = len(lines)

    while i < N:
        line = lines[i]

        # 0) collapse accidental six-quotes anywhere on the line
        new_line = RX_SIX_QUOTES.sub('"""', line)
        if new_line != line:
            changed = True
            line = new_line

        # 1) handle assignments that start a multiline string via ""\ (broken)
        m = RX_EQ_EMPTY_BACKSLASH.match(line)
        if m:
            prefix = m.group("prefix")
            # start a raw triple-quoted block
            out.append(f'{prefix}r"""\n')
            changed = True
            i += 1
            # consume following continuation lines until we reach a sensible end:
            # stop when we hit a line that *doesn't* end with backslash continuation
            # we include lines verbatim but strip a single trailing backslash
            while i < N:
                cur = lines[i]
                # also normalize six-quotes inside the body
                cur = RX_SIX_QUOTES.sub('"""', cur)
                if cur.rstrip().endswith("\\"):
                    # drop the trailing backslash and keep content
                    out.append(cur.rstrip()[:-1] + "\n")
                    i += 1
                    continue
                else:
                    # final line of the block – write it, then close the triple string
                    out.append(cur)
                    # ensure newline before closing if final line doesn’t end with newline
                    if not out[-1].endswith("\n"):
                        out[-1] = out[-1] + "\n"
                    out.append('"""\n')
                    break
            else:
                # file ended; still close the string safely
                out.append('"""\n')
            # advance main loop past what we consumed
            i += 1
            continue

        # 2) clean up stray lines that are just triple quotes (dangling opens)
        if RX_TRIPLE_OPEN_AT_END.match(line):
            # if the next non-empty, non-comment line is also a triple end, keep; else, make it a docstring on one line
            j = i + 1
            while j < N and (
                lines[j].strip() == "" or lines[j].lstrip().startswith("#")
            ):
                j += 1
            if j >= N or not RX_TRIPLE_OPEN_AT_END.match(lines[j].rstrip()):
                # make it an empty docstring so parsing can proceed
                out.append('"""\\n"""\n')
                changed = True
                i += 1
                continue

        out.append(line)
        i += 1

    if changed:
        dst = os.path.join(BACKUP, os.path.relpath(path, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(out)

    return changed


def main():
    if not os.path.exists(LIST):
        print("Missing compile_failures.tsv; run tools/list_compile_failures.py first.")
        return

    processed = 0
    fixed_compile = 0
    with open(LIST, "r", encoding="utf-8") as f:
        next(f, None)
        for line in f:
            p = line.split("\t", 1)[0].strip()
            if not p.endswith(".py") or not os.path.exists(p):
                continue
            processed += 1
            # only try to fix files that currently fail
            if compiles(p):
                continue
            changed = fix_file(p)
            if changed and compiles(p):
                fixed_compile += 1

    print(f"Processed: {processed}, now compiling after fix: {fixed_compile}")
    print("Backups:", BACKUP)


if __name__ == "__main__":
    main()
