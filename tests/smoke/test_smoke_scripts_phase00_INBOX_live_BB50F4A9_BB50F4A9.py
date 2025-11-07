import importlib, types


def test_import_scripts_phase00_INBOX_live_BB50F4A9_BB50F4A9():
    mod = importlib.import_module("scripts.phase00.INBOX.live_BB50F4A9_BB50F4A9")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
