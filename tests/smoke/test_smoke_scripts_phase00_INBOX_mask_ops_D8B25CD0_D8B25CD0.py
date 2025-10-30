import importlib, types


def test_import_scripts_phase00_INBOX_mask_ops_D8B25CD0_D8B25CD0():
    mod = importlib.import_module("scripts.phase00.INBOX.mask_ops_D8B25CD0_D8B25CD0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
