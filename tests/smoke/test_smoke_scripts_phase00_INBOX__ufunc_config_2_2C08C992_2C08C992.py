import importlib, types


def test_import_scripts_phase00_INBOX__ufunc_config_2_2C08C992_2C08C992():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._ufunc_config_2_2C08C992_2C08C992"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
