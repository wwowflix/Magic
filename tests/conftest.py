import os
import sys

ws = os.getenv("GITHUB_WORKSPACE")
if ws and ws not in sys.path:
    sys.path.insert(0, ws)
