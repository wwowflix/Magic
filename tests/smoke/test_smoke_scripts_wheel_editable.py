import importlib, types


def test_import_scripts_wheel_editable():
    mod = importlib.import_module("scripts.wheel_editable")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
