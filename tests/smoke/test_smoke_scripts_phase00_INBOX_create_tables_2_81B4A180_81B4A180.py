import importlib, types

def test_import_scripts_phase00_INBOX_create_tables_2_81B4A180_81B4A180():
    mod = importlib.import_module("scripts.phase00.INBOX.create_tables_2_81B4A180_81B4A180")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
