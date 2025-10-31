#!/usr/bin/env python
import sys  # noqa: I001
import re
import os

# pre-commit passes only staged files by default
BLOCK_EXT = re.compile(r"\.(exe|msi|whl|zip|7z|iso|dll)$", re.IGNORECASE)

bad = []
for p in sys.argv[1:]:
    # ignore deleted/renamed-if-missing paths
    if not os.path.exists(p):
        continue
    if BLOCK_EXT.search(p):
        bad.append(p)

if bad:
    sys.stderr.write(
        "BLOCKED: binary installer/artifact detected.\n"Please use GitHub Releases or Git LFS for these files.\n"Files:\n  - " + "\n  - ".join(bad) + "\n"
    )
    sys.exit(1)
sys.exit(0)
