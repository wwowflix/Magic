import importlib, types

def test_import_scripts_phase00_INBOX_mklabels_C647DB5E_C647DB5E():
    mod = importlib.import_module("scripts.phase00.INBOX.mklabels_C647DB5E_C647DB5E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
