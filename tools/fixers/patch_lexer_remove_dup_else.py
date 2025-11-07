#!/usr/bin/env python3
import pathlib  # noqa: I001
import ast
import sys

p = pathlib.Path("scripts/lexer.py")
txt = p.read_text(encoding="utf-8", errors="replace")
lines = txt.splitlines()


def is_bad_triple(i: int) -> bool:
    # matches:
    # else:
    #     if text.startswith("\"):
    #         text = text[len("\"):]
    if i + 2 >= len(lines):
        return False
    if lines[i].strip() != "else:":
        return False
    l1 = lines[i + 1].strip()
    l2 = lines[i + 2].strip()
    return ('startswith("\\")' in l1) and ('len("\\")' in l2)


out = []
i = 0
removed = 0
while i < len(lines):
    if is_bad_triple(i):
        i += 3
        removed += 1
        continue
    out.append(lines[i])
    i += 1

new = "\n".join(out) + ("\n" if not txt.endswith("\n") else "")

# sanity: must parse
try:
    ast.parse(new)
except Exception as e:
    print("PATCH FAILED (kept original):", e)
    sys.exit(1)

if new != txt:
    p.write_text(new, encoding="utf-8")
    print(f"lexer: removed {removed} bad else-block(s)")
else:
    print("lexer: no changes")
