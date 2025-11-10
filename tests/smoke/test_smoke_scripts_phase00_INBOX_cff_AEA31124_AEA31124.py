import importlib, types


def test_import_scripts_phase00_INBOX_cff_AEA31124_AEA31124():
    mod = importlib.import_module("scripts.phase00.INBOX.cff_AEA31124_AEA31124")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
