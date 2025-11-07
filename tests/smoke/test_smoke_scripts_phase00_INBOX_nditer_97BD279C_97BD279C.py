import importlib, types


def test_import_scripts_phase00_INBOX_nditer_97BD279C_97BD279C():
    mod = importlib.import_module("scripts.phase00.INBOX.nditer_97BD279C_97BD279C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
