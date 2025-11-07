import importlib, types


def test_import_scripts_phase00_INBOX__ranges_B3E1C71B_B3E1C71B():
    mod = importlib.import_module("scripts.phase00.INBOX._ranges_B3E1C71B_B3E1C71B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
