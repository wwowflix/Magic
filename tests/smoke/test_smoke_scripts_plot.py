import importlib, types


def test_import_scripts_plot():
    mod = importlib.import_module("scripts.plot")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
