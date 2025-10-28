import importlib, types

def test_import_scripts_phase00_INBOX_schemapi_C6046F1C_C6046F1C():
    mod = importlib.import_module("scripts.phase00.INBOX.schemapi_C6046F1C_C6046F1C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
