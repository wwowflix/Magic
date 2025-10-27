import argparse, os, sys, importlib, pkgutil, pathlib, textwrap

TEMPLATE = """\
import importlib, types

def test_import_{name_sanitized}():
    mod = importlib.import_module("{module}")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
"""

def sanitize(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch=="_" else "_" for ch in name)

def write_test(dst_dir: pathlib.Path, module: str):
    name = sanitize(module)
    path = dst_dir / f"test_smoke_{name}.py"
    path.write_text(TEMPLATE.format(name_sanitized=name, module=module), encoding="utf-8", newline="\n")
    return path

def guess_module(root: pathlib.Path, file: pathlib.Path) -> str | None:
    try:
        rel = file.relative_to(root).with_suffix("")
        parts = list(rel.parts)
        # drop non-package segments before real python roots if needed
        # heuristic: stop at first 'scripts' or 'tools'
        if "scripts" in parts:
            parts = parts[parts.index("scripts"):]
        elif "tools" in parts:
            parts = parts[parts.index("tools"):]
        return ".".join(parts)
    except Exception:
        return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="E:/MAGIC")
    p.add_argument("--glob", default="scripts/**/*.py;tools/**/*.py")
    p.add_argument("--out", default="tests/smoke")
    args = p.parse_args()

    root = pathlib.Path(args.root)
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)

    globs = [g.strip() for g in args.glob.split(";") if g.strip()]
    created = 0
    for g in globs:
        for f in root.glob(g):
            if f.name.startswith("test_"):
                continue
            mod = guess_module(root, f)
            if not mod:
                continue
            path = write_test(out, mod)
            created += 1
            print(f"[+] {path}")
    print(f"\nCreated {created} smoke tests in {out}")

if __name__ == "__main__":
    main()
