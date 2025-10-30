import importlib, types


def test_import_scripts_format_control():
    mod = importlib.import_module("scripts.format_control")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
