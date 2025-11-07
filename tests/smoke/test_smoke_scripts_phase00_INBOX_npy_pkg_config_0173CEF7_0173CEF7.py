import importlib, types


def test_import_scripts_phase00_INBOX_npy_pkg_config_0173CEF7_0173CEF7():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.npy_pkg_config_0173CEF7_0173CEF7"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
