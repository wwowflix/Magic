import importlib, types


def test_import_scripts_phase00_INBOX_setuponly_06B465C3_06B465C3():
    mod = importlib.import_module("scripts.phase00.INBOX.setuponly_06B465C3_06B465C3")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
