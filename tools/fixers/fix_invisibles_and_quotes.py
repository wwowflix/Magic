"""MAGIC: fix invisibles and smart quotes (clean)."""

SMART = {
    "“": '"',
    "”": '"',
    "„": '"',
    "’": "'",
    "‘": "'",
    "—": "-",
    "–": "-",
}

INVISIBLES = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u00a0"]

def fix_line(line: str) -> str:
    for ch in INVISIBLES:
        line = line.replace(ch, "")
    for bad, good in SMART.items():
        line = line.replace(bad, good)
    return line

def fix_text(text: str) -> str:
    return "\n".join(fix_line(ln) for ln in text.splitlines())
