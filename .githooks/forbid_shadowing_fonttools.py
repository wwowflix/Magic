import sys
import os

bad = []
for name in ("scripts/otTables.py", "scripts/otConverters.py"):
    if os.path.exists(name):
        bad.append(name)
if bad:
    print("Shadowing files found in scripts/:", ", ".join(bad))
    sys.exit(1)
