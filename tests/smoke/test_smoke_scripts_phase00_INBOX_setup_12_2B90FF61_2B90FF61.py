import importlib, types


def test_import_scripts_phase00_INBOX_setup_12_2B90FF61_2B90FF61():
    mod = importlib.import_module("scripts.phase00.INBOX.setup_12_2B90FF61_2B90FF61")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
