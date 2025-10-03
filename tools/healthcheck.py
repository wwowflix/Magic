#!/usr/bin/env python3
import sys, os

must_exist = [
    "requirements.txt",
    "scripts/phase0/0A_sorter_READY.py",
    "tools/magic_acceptance.ps1",
]

missing = [p for p in must_exist if not os.path.exists(p)]
if missing:
    print("HC FAIL: missing:", ", ".join(missing))
    sys.exit(1)

print("HC OK")
