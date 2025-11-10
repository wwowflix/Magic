import importlib, types


def test_import_scripts_phase00_INBOX_tutil_B3DE0556_B3DE0556():
    mod = importlib.import_module("scripts.phase00.INBOX.tutil_B3DE0556_B3DE0556")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
