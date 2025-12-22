import importlib, sys, os

print("=== sys.path dump ===")
for p in sys.path:
    print(" ", repr(p))

print("\n=== IMPORT TEST ===")
try:
    mod = importlib.import_module("fsspec")
    print("fsspec.__file__ =", getattr(mod, "__file__", "<namespace>"))
except Exception as e:
    print("FAILED TO IMPORT fsspec:", e)

print("\n=== Checking sys.path for fsspec folders ===")
for path in sys.path:
    fp = os.path.join(path, "fsspec")
    if os.path.exists(fp):
        print("FOUND:", fp)
