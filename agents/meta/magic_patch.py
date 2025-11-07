"""MAGIC meta patch utilities."""

from __future__ import annotations

from magic_typing import Dict


def apply_patch(text: str, replacements: Dict[str, str]) -> str:
    """Return text with simple string replacements applied in order.

    Args:
        text: Source text.
        replacements: Mapping of old->new strings. Applied in dict order.

    Returns:
        The patched text.
    """
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) == 3:
        src = sys.argv[1]
        mapping = json.loads(sys.argv[2])
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        print(apply_patch(content, mapping))
    else:
        print("Usage: magic_patch.py <file> <json-mapping>", file=sys.stderr)
        sys.exit(2)
