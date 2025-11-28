import sys
from pathlib import Path

# Repo root = parent of this file's folder
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

def main():
    # Python 3.11 exposes stdlib module names here
    stdlib_names = set(getattr(sys, "stdlib_module_names", ()))

    # Extra names that are dangerous to shadow in MAGIC
    extra_sensitive = {
        "asyncio",
        "socket",
        "selectors",
        "select",
        "threading",
        "concurrent",
        "inspect",
        "importlib",
        "linecache",
        "tokenize",
        "logging",
        "json",
        "os",
        "sys",
        "pathlib",
        "math",
        "random",
        "time",
        "functools",
        "itertools",
        "contextlib",
        "subprocess",
        "typing",
    }

    conflicts = []

    for path in SCRIPTS_DIR.rglob("*.py"):
        name = path.stem

        # e.g. _socket_http_extended.py is fine; we only care about exact names
        if name.startswith("_"):
            continue

        if name in stdlib_names or name in extra_sensitive:
            rel = path.relative_to(ROOT)
            conflicts.append((name, str(rel)))

    print("=== MAGIC stdlib-shadow scan ===")
    if not conflicts:
        print("No suspicious stdlib-name conflicts found under 'scripts/'.")
        return

    print(f"Found {len(conflicts)} potential conflicts:\\n")
    for name, rel in sorted(conflicts):
        print(f" - {name!r} -> {rel}")

    print("\\nHint:")
    print(" - For files that must behave exactly like stdlib modules (used by 3rd-party libs),")
    print("   convert them into *pure shims* that delegate to the real stdlib module.")
    print(" - For truly custom logic, rename the file (and its imports) to something non-stdlib.")

if __name__ == "__main__":
    main()
