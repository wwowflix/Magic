import importlib, types

def test_import_scripts_phase00_INBOX__functools_3EC636FB_3EC636FB():
    mod = importlib.import_module("scripts.phase00.INBOX._functools_3EC636FB_3EC636FB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
