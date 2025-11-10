import importlib, types


def test_import_scripts_phase00_INBOX_sbcharsetprober_FA777717_FA777717():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.sbcharsetprober_FA777717_FA777717"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
