"""MAGIC: auto-fix broken unicode quotes."""

SMART = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
}

INVIS = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060", "\u00a0"]

def normalize_text(txt: str) -> str:
    for ch in INVIS:
        txt = txt.replace(ch, "")
    for bad, good in SMART.items():
        txt = txt.replace(bad, good)
    return txt.replace("\r\n", "\n").replace("\r", "\n")
