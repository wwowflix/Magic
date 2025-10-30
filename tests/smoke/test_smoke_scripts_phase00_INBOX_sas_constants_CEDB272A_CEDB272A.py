import importlib, types


def test_import_scripts_phase00_INBOX_sas_constants_CEDB272A_CEDB272A():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.sas_constants_CEDB272A_CEDB272A"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
