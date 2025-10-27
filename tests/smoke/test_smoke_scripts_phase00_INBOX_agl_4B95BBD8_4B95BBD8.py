import importlib, types

def test_import_scripts_phase00_INBOX_agl_4B95BBD8_4B95BBD8():
    mod = importlib.import_module("scripts.phase00.INBOX.agl_4B95BBD8_4B95BBD8")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
