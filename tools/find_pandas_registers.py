import os
import re

ROOT = r"E:\MAGIC\scripts"
pattern = re.compile(r"register_option\s*\(")

matches = []

for dirpath, _, filenames in os.walk(ROOT):
    for f in filenames:
        if not f.endswith(".py"):
            continue
        path = os.path.join(dirpath, f)
        try:
            text = open(path, "r", encoding="utf8").read()
        except:
            continue
        if pattern.search(text):
            matches.append(path)

print("=== Files containing register_option(...) ===")
for m in matches:
    print(" -", m)

if not matches:
    print("No files found.")
