import importlib, types

def test_import_scripts_phase00_INBOX_file_not_found_test_2737003A_2737003A():
    mod = importlib.import_module("scripts.phase00.INBOX.file_not_found_test_2737003A_2737003A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
