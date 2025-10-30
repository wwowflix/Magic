import importlib, types


def test_import_scripts_phase00_INBOX_threadpoolctl_12FB9526_12FB9526():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.threadpoolctl_12FB9526_12FB9526"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
