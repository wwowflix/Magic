import importlib, types


def test_import_scripts_line_break():
    mod = importlib.import_module("scripts.line_break")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
