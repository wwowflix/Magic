import importlib, types

def test_import_scripts_phase00_INBOX_api_FD96FD39_FD96FD39():
    mod = importlib.import_module("scripts.phase00.INBOX.api_FD96FD39_FD96FD39")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
