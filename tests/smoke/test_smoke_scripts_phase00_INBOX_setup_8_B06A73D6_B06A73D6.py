import importlib, types


def test_import_scripts_phase00_INBOX_setup_8_B06A73D6_B06A73D6():
    mod = importlib.import_module("scripts.phase00.INBOX.setup_8_B06A73D6_B06A73D6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
