import importlib, types


def test_import_scripts_phase00_INBOX_redditors_8F4394AE_8F4394AE():
    mod = importlib.import_module("scripts.phase00.INBOX.redditors_8F4394AE_8F4394AE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
