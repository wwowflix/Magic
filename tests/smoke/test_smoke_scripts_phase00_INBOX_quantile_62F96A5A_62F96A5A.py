import importlib, types


def test_import_scripts_phase00_INBOX_quantile_62F96A5A_62F96A5A():
    mod = importlib.import_module("scripts.phase00.INBOX.quantile_62F96A5A_62F96A5A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
