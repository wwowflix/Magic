import difflib, os
from pathlib import Path

OUT_PATCH = Path(os.environ.get("MAGIC_ROOT",".")) / "outputs" / "remediation" / "patches"

def make_diff(original_text: str, new_text: str, fname: str):
    a = (original_text or "").splitlines(keepends=True)
    b = (new_text or "").splitlines(keepends=True)
    diff = difflib.unified_diff(a, b, fromfile=fname, tofile=fname + ".AI", lineterm="")
    return "".join(diff)

def write_diff(script_path: str, new_text: str):
    p = Path(script_path)
    try:
        old = p.read_text(encoding="utf-8")
    except Exception:
        old = ""
    d = make_diff(old, new_text, p.name)
    OUT_PATCH.mkdir(parents=True, exist_ok=True)
    out = OUT_PATCH / (p.stem + ".diff")
    out.write_text(d, encoding="utf-8")
    return str(out), len(d)
