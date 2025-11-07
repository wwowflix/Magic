import importlib, types


def test_import_scripts_phase00_INBOX_ufunc_config_B65BCF40_B65BCF40():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.ufunc_config_B65BCF40_B65BCF40"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
