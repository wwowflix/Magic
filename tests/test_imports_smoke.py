import importlib, pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "scripts"
for py in sorted(SRC.rglob("*.py")):
    rel = py.relative_to(SRC).with_suffix("")
    mod = "scripts." + str(rel).replace("\\", ".").replace("/", ".")
    if "__pycache__" in mod or mod.endswith(".__init__"):
        continue
    importlib.import_module(mod)
