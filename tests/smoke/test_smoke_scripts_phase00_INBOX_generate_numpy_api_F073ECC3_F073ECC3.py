import importlib, types


def test_import_scripts_phase00_INBOX_generate_numpy_api_F073ECC3_F073ECC3():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.generate_numpy_api_F073ECC3_F073ECC3"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
