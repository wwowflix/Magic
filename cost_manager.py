import os, sys

# add ./src to sys.path so `import magic...` works in a src/ layout
root = os.path.dirname(__file__)
src = os.path.join(root, "src")
if os.path.isdir(src) and src not in sys.path:
    sys.path.insert(0, src)

try:
    from scripts.cost_manager import *  # legacy location
except ModuleNotFoundError:
    from magic.cost_manager import *    # src/ layout
