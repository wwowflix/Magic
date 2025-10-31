"""MAGIC: utf8 repair helper (clean version)."""

SMART_MAP = {
    "–": "-",
    "—": "-",
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "…": "...",
    " ": " ",  # NBSP -> space
}

def fix_text(s: str) -> str:
    for bad, good in SMART_MAP.items():
        s = s.replace(bad, good)
    return s
