import importlib, types

def test_import_scripts_phase00_INBOX__make_2_0B1321E5_0B1321E5():
    mod = importlib.import_module("scripts.phase00.INBOX._make_2_0B1321E5_0B1321E5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
