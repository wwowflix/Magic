import importlib, types


def test_import_scripts_algorithms_3():
    mod = importlib.import_module("scripts.algorithms_3")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
