import importlib, sys

targets = [
    "scripts._a_v_a_r",
    "scripts._asyncgens",
    "scripts.core",
]
failed = 0
for name in targets:
    try:
        importlib.import_module(name)
        print("OK", name)
    except Exception as e:
        print("FAIL", name, e)
        failed += 1
sys.exit(1 if failed else 0)
