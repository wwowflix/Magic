import argparse
import os
import re
import sys
from typing import Dict

# Common Windows-1252/UTF-8 mojibake sequences -> proper Unicode
MOJIBAKE_MAP: Dict[str, str] = {
    # punctuation / quotes / dashes
    "â€”": "—",
    "â€“": "–",
    "â€˜": "‘",
    "â€™": "’",
    "â€œ": "“",
    "â€�": "”",
    "â€¦": "…",
    "â€¢": "•",
    "â€¡": "‡",
    "â€": "”",  # sometimes appears as a stray “double-quote”
    # mis-encoded Latin letters noise
    "Ã—": "×",
    "ÃŸ": "ß",
    "Ã†": "Æ",
    "Ã˜": "Ø",
    "Ã¥": "å",
    "Ã¤": "ä",
    "Ã¶": "ö",
    "Ã¼": "ü",
    "Ã©": "é",
    "Ã¨": "è",
    "Ãª": "ê",
    "Ãº": "ú",
    "Ã³": "ó",
    "Ã²": "ò",
    "Ã­": "í",
    "Ã¡": "á",
    "Ã£": "ã",
    "Ãµ": "õ",
    "Ã¢": "â",
    "Ã´": "ô",
    "Ã§": "ç",
    "Ã¹": "ù",
    "Ã±": "ñ",
    # stray non-breaking space markers
    "Â ": "",
    "Â": "",
    # rare leftovers
    "â„¢": "™",
    "â‚¬": "€",
    "â€º": "›",
    "â€¹": "‹",
}


def strip_bom(text: str) -> str:
    if text.startswith("\ufeff"):
        return text.lstrip("\ufeff")
    return text


def demojibake(text: str) -> str:
    # Apply direct replacements
    for bad, good in MOJIBAKE_MAP.items():
        if bad in text:
            text = text.replace(bad, good)
    # Fix accidental double-encoding like "â€\"" around quotes if any remain
    text = re.sub(r"â€\s*", '"', text)
    # Collapse repeated accidental bytes
    text = text.replace("Ã‚", "").replace("Ã", "")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--file", required=True, help="Path to a .py file to normalize/fix."
    )
    args = ap.parse_args()
    path = args.file

    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        sys.exit(2)

    raw = open(path, "rb").read()

    # Try utf-8 / utf-8-sig first
    decoded = None
    for enc in ("utf-8", "utf-8-sig"):
        try:
            decoded = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue

    # If still failing, fallback to latin-1 then treat as text to clean
    if decoded is None:
        decoded = raw.decode("latin-1")

    # Strip BOM and run mojibake cleaner
    cleaned = strip_bom(decoded)
    cleaned = demojibake(cleaned)

    # Ensure file ends with a single newline, avoid trailing CRLF chaos
    cleaned = re.sub(r"\r\n", "\n", cleaned)  # normalize to LF
    if not cleaned.endswith("\n"):
        cleaned += "\n"

    # Write back in UTF-8 (no BOM)
    with open(path, "wb") as f:
        f.write(cleaned.encode("utf-8"))

    print(f"✅ Repaired & normalized: {path}")


if __name__ == "__main__":
    main()
