import importlib, types


def test_import_scripts_phase00_INBOX__config_4_746AB7C5_746AB7C5():
    mod = importlib.import_module("scripts.phase00.INBOX._config_4_746AB7C5_746AB7C5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
