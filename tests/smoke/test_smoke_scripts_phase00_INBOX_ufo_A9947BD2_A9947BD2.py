import importlib, types

def test_import_scripts_phase00_INBOX_ufo_A9947BD2_A9947BD2():
    mod = importlib.import_module("scripts.phase00.INBOX.ufo_A9947BD2_A9947BD2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
