import importlib, types


def test_import_scripts_phase00_INBOX_performance_F76EBB8D_F76EBB8D():
    mod = importlib.import_module("scripts.phase00.INBOX.performance_F76EBB8D_F76EBB8D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
