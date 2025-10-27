import importlib, types

def test_import_scripts_phase00_INBOX_interpolatableTestContourOrder_98727D47_98727D47():
    mod = importlib.import_module("scripts.phase00.INBOX.interpolatableTestContourOrder_98727D47_98727D47")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
