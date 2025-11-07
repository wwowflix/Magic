import importlib, types


def test_import_scripts_phase00_INBOX_package_index_80B298B2_80B298B2():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.package_index_80B298B2_80B298B2"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
