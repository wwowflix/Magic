import importlib, types


def test_import_scripts_cu2quPen():
    mod = importlib.import_module("scripts.cu2quPen")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
