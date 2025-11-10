import importlib, types


def test_import_scripts_phase00_INBOX_masked_reductions_13A7B286_13A7B286():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.masked_reductions_13A7B286_13A7B286"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
