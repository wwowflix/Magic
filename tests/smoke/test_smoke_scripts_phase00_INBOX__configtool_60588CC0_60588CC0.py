import importlib, types


def test_import_scripts_phase00_INBOX__configtool_60588CC0_60588CC0():
    mod = importlib.import_module("scripts.phase00.INBOX._configtool_60588CC0_60588CC0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
