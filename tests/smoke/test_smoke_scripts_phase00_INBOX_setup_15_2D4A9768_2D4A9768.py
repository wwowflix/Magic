import importlib, types


def test_import_scripts_phase00_INBOX_setup_15_2D4A9768_2D4A9768():
    mod = importlib.import_module("scripts.phase00.INBOX.setup_15_2D4A9768_2D4A9768")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
