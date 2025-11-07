import importlib, types


def test_import_scripts_explicitClosingLinePen():
    mod = importlib.import_module("scripts.explicitClosingLinePen")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
