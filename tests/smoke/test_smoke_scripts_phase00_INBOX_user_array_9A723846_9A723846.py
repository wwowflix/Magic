import importlib, types


def test_import_scripts_phase00_INBOX_user_array_9A723846_9A723846():
    mod = importlib.import_module("scripts.phase00.INBOX.user_array_9A723846_9A723846")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
