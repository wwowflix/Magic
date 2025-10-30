import os, importlib, traceback, sys

mods = ["scripts._abnf", "scripts._events", "scripts._state", "scripts._connection"]
fail = 0

print("=== QUICK IMPORT CHECK ===")
for m in mods:
    try:
        importlib.invalidate_caches()
        mod = importlib.import_module(m)
        path = getattr(mod, "__file__", None)
        # no f-strings; no backslashes in {...} expressions
        print("{:<24} OK   -> {}".format(m, path))
    except Exception as e:
        fail += 1
        print("{:<24} FAIL -> {}: {}".format(m, e.__class__.__name__, e))
        traceback.print_exc()

strict = os.getenv("MAGIC_STRICT", "0") == "1"
if strict and fail:
    sys.exit("STRICT FAIL: {}/{} failed".format(fail, len(mods)))
