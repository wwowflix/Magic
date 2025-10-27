import importlib, types

def test_import_tools_remediator():
    mod = importlib.import_module("tools.remediator")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
