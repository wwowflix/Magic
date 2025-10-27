import importlib, types

def test_import_scripts_phase00_INBOX_ufuncs_BBD6DB36_BBD6DB36():
    mod = importlib.import_module("scripts.phase00.INBOX.ufuncs_BBD6DB36_BBD6DB36")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
