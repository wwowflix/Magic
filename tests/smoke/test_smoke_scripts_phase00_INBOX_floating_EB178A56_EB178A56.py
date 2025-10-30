import importlib, types


def test_import_scripts_phase00_INBOX_floating_EB178A56_EB178A56():
    mod = importlib.import_module("scripts.phase00.INBOX.floating_EB178A56_EB178A56")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
