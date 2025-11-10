import importlib, types


def test_import_scripts_phase00_INBOX_scipy_sparse_9C5C2514_9C5C2514():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.scipy_sparse_9C5C2514_9C5C2514"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
