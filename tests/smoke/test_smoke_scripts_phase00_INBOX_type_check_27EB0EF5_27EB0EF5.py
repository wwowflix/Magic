import importlib, types

def test_import_scripts_phase00_INBOX_type_check_27EB0EF5_27EB0EF5():
    mod = importlib.import_module("scripts.phase00.INBOX.type_check_27EB0EF5_27EB0EF5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
