import importlib, types


def test_import_scripts_phase00_INBOX_diff_A5A520A8_A5A520A8():
    mod = importlib.import_module("scripts.phase00.INBOX.diff_A5A520A8_A5A520A8")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
