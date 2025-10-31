"""MAGIC: round6 fixer (safe stub)."""

SMART = {
    "\u00a0": " ",  # NBSP -> space
}

def fix_block(text: str) -> str:
    for bad, good in SMART.items():
        text = text.replace(bad, good)
    return text
