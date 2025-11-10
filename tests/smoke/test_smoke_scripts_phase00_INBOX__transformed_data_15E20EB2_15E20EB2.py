import importlib, types


def test_import_scripts_phase00_INBOX__transformed_data_15E20EB2_15E20EB2():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._transformed_data_15E20EB2_15E20EB2"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
