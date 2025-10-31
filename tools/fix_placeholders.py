import pathlib

# Root folders to clean
ROOTS = [
    pathlib.Path("scripts"),
    pathlib.Path("tools"),
]

# Common mojibake → real characters
MOJIBAKE_MAP = {
    "✅": "✅",
    "—": "—",
    "–": "–",
    "'": "'",
    "'": "'",
    """: '"',
    """: '"',
}


def normalize_text(text: str) -> str:
    """Normalize text: drop BOMs, fix encoding, newlines, and trailing junk."""
    # normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # drop trailing lone triple-quote
    if text.rstrip().endswith('"""') and not text.rstrip().endswith('""""'):
        text = text.rstrip()[:-3].rstrip() + "\n"

    # apply mojibake fixes
    for bad, good in MOJIBAKE_MAP.items():
        if bad in text:
            text = text.replace(bad, good)

    # ensure trailing newline
    if not text.endswith("\n"):
        text += "\n"

    return text


def main() -> None:
    """Scan and fix all .py files under target roots."""
    changed = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.py"):
            raw = p.read_text(encoding="utf-8", errors="replace")
            fixed = normalize_text(raw.lstrip("\ufeff"))
            if fixed != raw:
                p.write_text(fixed, encoding="utf-8")
                changed += 1
    print(f"✅ Placeholder/docstring fixes applied to {changed} files.")


if __name__ == "__main__":
    main()
