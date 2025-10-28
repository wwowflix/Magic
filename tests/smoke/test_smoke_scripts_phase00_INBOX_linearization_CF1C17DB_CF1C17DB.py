import importlib, types

def test_import_scripts_phase00_INBOX_linearization_CF1C17DB_CF1C17DB():
    mod = importlib.import_module("scripts.phase00.INBOX.linearization_CF1C17DB_CF1C17DB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
