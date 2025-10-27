import importlib, types

def test_import_scripts_phase00_INBOX_range_6593E8D0_6593E8D0():
    mod = importlib.import_module("scripts.phase00.INBOX.range_6593E8D0_6593E8D0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
