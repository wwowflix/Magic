import sys, os


def has_bom(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(3) == b"\xef\xbb\xbf"
    except Exception:
        return False


bad = []
for p in sys.argv[1:]:
    # Only check Python sources
    if not p.lower().endswith(".py"):
        continue
    if has_bom(p):
        bad.append(p)

if bad:
    sys.stderr.write("UTF-8 BOM found in:\\n" + "\\n".join(bad) + "\\n")
    sys.exit(2)
sys.exit(0)
