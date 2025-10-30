import importlib, types


def test_import_scripts_phase00_INBOX_link_9DFC9B55_9DFC9B55():
    mod = importlib.import_module("scripts.phase00.INBOX.link_9DFC9B55_9DFC9B55")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
