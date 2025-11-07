#!/usr/bin/env python3
import re  # noqa: I001
import pathlib

p = pathlib.Path("scripts/lexer.py")
src = p.read_text(encoding="utf-8", errors="replace")

# We surgically normalize the 191–197 window.
# Replace any malformed backslash checks/slices with a clean block.
pattern = re.compile(
    r"""
    (^[ \t]*else:\s*\n         # line 191
     [ \t]*text\s*=\s*text\.decode\(\s*self\.encoding\s*\)\s*\n  # line 192
     [\s\S]{0,200}?            # the next few broken lines we will replace
    )
    """,
    re.VERBOSE | re.MULTILINE,
)

replacement = (
    "            else:\n"                text = text.decode(self.encoding)\n"
    '                if text.startswith("\\\\"):\n'
    '                    text = text[len("\\\\"):]\n'
)

# A second else-block sometimes follows immediately; normalize that too if present.
# We ensure a consistent second branch:
post_fix = (
    "            else:\n"
    '                if text.startswith("\\\\"):\n'
    '                    text = text[len("\\\\"):]\n'
)

# First, patch the first else-block
m = pattern.search(src)
if m:
    start = m.start(1)
    # Find the following 'else:' that corresponds to the non-bytes branch (line ~195)
    tail = src[m.end(1) :]
    m_else2 = re.search(r"^[ \t]*else:\s*$", tail, re.MULTILINE)
    if m_else2:
        # splice: [prefix] + replacement + [from else2:] with normalized block
        prefix = src[:start]
        rest = tail[m_else2.start() :]
        # ensure the second block is normalized (replace its first two lines)
        rest = re.sub(
            r"^[ \t]*else:\s*\n[ \t]*if\s+text\.startswith\([^\n]*\)\s*:\s*\n[ \t]*text\s*=\s*text\[.*?\]\s*\n",  # noqa: E501
            post_fix,
            rest,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        new_src = prefix + replacement + rest
        if new_src != src:
            p.write_text(new_src, encoding="utf-8")
            print("LEXER_PATCH applied")
        else:
            print("LEXER_PATCH nochange")
    else:
        # If we didn't find the second else:, still apply the first fix
        new_src = src[:start] + replacement + src[m.end(1) :]
        if new_src != src:
            p.write_text(new_src, encoding="utf-8")
            print("LEXER_PATCH applied (partial)")
        else:
            print("LEXER_PATCH nochange (partial)")
else:
    # fallback: do minimal token fixes
    s2 = src
    s2 = s2.replace('startswith("\\")', 'startswith("\\\\")')
    s2 = s2.replace('len("\\") :]', 'len("\\\\"):]')
    s2 = s2.replace('len("\\") :', 'len("\\\\"):')
    if s2 != src:
        p.write_text(s2, encoding="utf-8")
        print("LEXER_MINIMAL applied")
    else:
        print("LEXER not matched; no changes")
