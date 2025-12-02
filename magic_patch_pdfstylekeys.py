from __future__ import annotations

import pathlib

ROOT = pathlib.Path(r"E:\MAGIC")
ENUM_FILE = ROOT / "scripts" / "enums.py"

MARKER = "MAGIC PDFStyleKeys shim"

def main() -> None:
    text = ENUM_FILE.read_text(encoding="utf-8")

    if MARKER in text:
        print("MAGIC: PDFStyleKeys already shimmed, nothing to do.")
        return

    # Find the existing PDFStyleKeys declaration
    needle = "class PDFStyleKeys"
    idx = text.find(needle)
    if idx == -1:
        raise SystemExit("Could not find 'class PDFStyleKeys' in enums.py")

    lines = text.splitlines(keepends=True)

    # Work out which line index holds the class definition
    start_line = None
    running_len = 0
    for i, line in enumerate(lines):
        running_len += len(line)
        if running_len > idx:
            start_line = i
            break

    if start_line is None:
        raise SystemExit("Internal error locating PDFStyleKeys start")

    # Determine indentation of the class block (e.g. "")
    first = lines[start_line]
    base_indent = first[: len(first) - len(first.lstrip())]

    # Collect until next top-level (same or less indent, starting with 'class ' or 'def ')
    end_line = len(lines)
    for j in range(start_line + 1, len(lines)):
        ln = lines[j]
        stripped = ln.lstrip()
        if not stripped:
            # blank line → might still be part of class, keep going
            continue
        indent = ln[: len(ln) - len(stripped)]
        if indent <= base_indent and stripped.startswith(("class ", "def ")):
            end_line = j
            break

    original_block = "".join(lines[start_line:end_line])

    print("=== MAGIC: original PDFStyleKeys block start ===")
    print(original_block)
    print("=== MAGIC: original PDFStyleKeys block end ===")

    shim_block = f'''{base_indent}# {MARKER}
{base_indent}class PDFStyleKeys:
{base_indent}    """
{base_indent}    MAGIC Week 0 shim for drawing.GraphicsStyle.
{base_indent}
{base_indent}    - Not an Enum.
{base_indent}    - Provides at least STROKE_ALPHA, FILL_ALPHA, BLEND_MODE.
{base_indent}    - Lazily creates any other uppercase key on demand so
{base_indent}      imports never fail.
{base_indent}    """
{base_indent}    _keys: dict[str, int] = {{}}
{base_indent}
{base_indent}    # Pre-seed the three keys we know drawing.py needs
{base_indent}    STROKE_ALPHA = 0
{base_indent}    FILL_ALPHA = 1
{base_indent}    BLEND_MODE = 2
{base_indent}    _keys.update({{'STROKE_ALPHA': 0, 'FILL_ALPHA': 1, 'BLEND_MODE': 2}})
{base_indent}
{base_indent}    @classmethod
{base_indent}    def __getattr__(cls, name: str):
{base_indent}        # Auto-create any missing ALL-CAPS keys
{base_indent}        if name.isupper():
{base_indent}            value = len(cls._keys)
{base_indent}            cls._keys[name] = value
{base_indent}            setattr(cls, name, value)
{base_indent}            return value
{base_indent}        raise AttributeError(name)
{base_indent}
{base_indent}    @classmethod
{base_indent}    def __iter__(cls):
{base_indent}        # Very light Enum-style iteration
{base_indent}        for key in sorted(cls._keys, key=cls._keys.get):
{base_indent}            yield getattr(cls, key)
{base_indent}
'''

    # Replace the block
    new_lines = lines[:start_line] + [shim_block] + lines[end_line:]
    ENUM_FILE.write_text("".join(new_lines), encoding="utf-8")

    print("MAGIC: Replaced PDFStyleKeys with shim class.")
    print(f"MAGIC: Patched file: {ENUM_FILE}")

if __name__ == "__main__":
    main()
