import importlib, types


def test_import_scripts_phase00_INBOX_multiarray_3_2C457236_2C457236():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.multiarray_3_2C457236_2C457236"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
