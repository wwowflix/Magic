import importlib, types

def test_import_scripts_phase00_INBOX_bcppcompiler_804D9A76_804D9A76():
    mod = importlib.import_module("scripts.phase00.INBOX.bcppcompiler_804D9A76_804D9A76")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
