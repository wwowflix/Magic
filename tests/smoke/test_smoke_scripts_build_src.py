import importlib, types


def test_import_scripts_build_src():
    mod = importlib.import_module("scripts.build_src")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
