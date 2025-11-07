import importlib, types


def test_import_scripts_phase00_INBOX_install_cxx_toolchain_1D37FE2C_1D37FE2C():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.install_cxx_toolchain_1D37FE2C_1D37FE2C"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
