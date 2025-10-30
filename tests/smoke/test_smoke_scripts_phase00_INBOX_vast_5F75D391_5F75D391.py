import importlib, types


def test_import_scripts_phase00_INBOX_vast_5F75D391_5F75D391():
    mod = importlib.import_module("scripts.phase00.INBOX.vast_5F75D391_5F75D391")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
