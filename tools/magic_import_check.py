import importlib
import pkgutil
import sys
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent  # E:\MAGIC
sys.path.insert(0, str(root))

results = []
failures = []

print("=== PYTHON scripts.* IMPORT CHECK START ===")

# Only look inside the "scripts" package
scripts_pkg_path = root / "scripts"

for mod in pkgutil.iter_modules([str(scripts_pkg_path)]):
    name = f"scripts.{mod.name}"
    try:
        importlib.import_module(name)
        line = "OK:" + name
        print(line)
        results.append(line)
    except Exception as e:
        line = f"FAIL:{name}:{e!r}"
        print(line)
        results.append(line)
        failures.append(line)

# Save results to a file at the repo root
out_path = root / "magic_imports_live_results.txt"
out_path.write_text("\\n".join(results), encoding="utf-8")

print("=== PYTHON scripts.* IMPORT CHECK END ===")

if failures:
    print("\\n[!] Import failures detected:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
else:
    print("\\nAll scripts.* modules imported successfully!")
    sys.exit(0)
