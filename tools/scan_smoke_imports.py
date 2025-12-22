"""
MAGIC Week 0 helper: scan all smoke-script imports and show which ones fail.

- Reads tests/smoke/test_smoke_scripts_*.py
- Extracts "scripts.<name>" from import_module() calls
- Tries to import each
- Prints a simple table with status + first error line
"""

import importlib
import pathlib
import re
from collections import defaultdict


ROOT = pathlib.Path(__file__).resolve().parents[1]
tests_dir = ROOT / "tests" / "smoke"

# Pattern to find: importlib.import_module("scripts.<name>")
IMPORT_PATTERN = re.compile(r'import_module\("scripts\.([a-zA-Z0-9_]+)"\)')

modules = set()

for path in sorted(tests_dir.glob("test_smoke_scripts_*.py")):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        continue
    for match in IMPORT_PATTERN.finditer(text):
        modules.add(match.group(1))

results = []

for name in sorted(modules):
    full_name = f"scripts.{name}"
    try:
        importlib.import_module(full_name)
    except Exception as e:  # noqa: BLE001 - we WANT any exception type
        err_type = type(e).__name__
        # Only first line of message for compact table
        msg = str(e).splitlines()[0] if str(e) else ""
        results.append((name, "FAIL", err_type, msg))
    else:
        results.append((name, "OK", "", ""))

# Print table
header = f"{'MODULE':35} {'STATUS':8} {'ERROR_TYPE':15} ERROR_MSG"
print(header)
print("-" * len(header))

for name, status, err_type, msg in results:
    print(f"{name:35} {status:8} {err_type:15} {msg}")

# Summary
fail_count = sum(1 for _, s, _, _ in results if s == "FAIL")
ok_count = sum(1 for _, s, _, _ in results if s == "OK")

print()
print(f"Total modules: {len(results)}")
print(f"OK:           {ok_count}")
print(f"Failing:      {fail_count}")
