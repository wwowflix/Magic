#!/usr/bin/env python3
import pathlib  # noqa: I001
import re
import ast
import sys

p = pathlib.Path("scripts/lexer.py")
src = p.read_text(encoding="utf-8", errors="replace")

# Replace the whole fragile window with a canonical, AST-safe version.
# We search for the decode(...) line and then normalize the next few lines.
pat = re.compile(
    r"""(?mx)
    ^(?P<i>\s*)else:\s*\n
    (?P=i)    text\s*=\s*text\.decode\(\s*self\.encoding\s*\)\s*\n
    (?P=tail)(?:.*\n){0,6}?      # up to a handful of the broken lines
    """
)
# Build normalized block with proper escaping.
block = (
    "else:\n"
    "    text = text.decode(self.encoding)\n"
    '    if text.startswith("\\\\"):\n'
    '        text = text[len("\\\\"):]\n'
)

m = pat.search(src)
if not m:
    print("PATCH: pattern not found; no changes")
    sys.exit(0)

start = m.start()
end = m.end()

new = src[:start] + block + src[end:]

# As a bonus, normalize a possible second 'else:' that often follows.
# If the next lines begin with 'else:' and have the same broken slice, fix them too.
post_pat = re.compile(
    r"(?m)^(?P<i>\s*)else:\s*\n(?P=i)    if\s+text\.startswith\([^\n]*\)\s*:\s*\n(?P=i)    text\s*=\s*text\[.*?\]\s*\n"  # noqa: E501
)
new = post_pat.sub(
    lambda m: (
        f"{m.group('i')}else:\n"
        f"{m.group('i')}    if text.startswith(\"\\\\\"):\n"
        f"{m.group('i')}        text = text[len(\"\\\\\"):]\n"
    ),
    new,
    count=1,
)

# Sanity: ensure it parses
try:
    ast.parse(new)
except Exception as e:
    print("PATCH: produced non-AST source:", e)
    sys.exit(1)

p.write_text(new, encoding="utf-8")
print("PATCH: lexer window normalized")
