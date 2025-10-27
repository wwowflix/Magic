import importlib, types

def test_import_scripts_setuptools_build():
    mod = importlib.import_module("scripts.setuptools_build")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
