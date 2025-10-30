import importlib, types


def test_import_scripts_phase00_INBOX_lahey_B02273AB_B02273AB():
    mod = importlib.import_module("scripts.phase00.INBOX.lahey_B02273AB_B02273AB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
