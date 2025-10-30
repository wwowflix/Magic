import importlib, types


def test_import_tools_drill_restore_from_latest():
    mod = importlib.import_module("tools.drill.restore_from_latest")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
