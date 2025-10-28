import importlib, types

def test_import_scripts_phase00_INBOX_jisfreq_9A6F2D7E_9A6F2D7E():
    mod = importlib.import_module("scripts.phase00.INBOX.jisfreq_9A6F2D7E_9A6F2D7E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
