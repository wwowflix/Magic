import importlib, types


def test_import_scripts_phase00_INBOX_generate_patch_csv_62973F09_62973F09():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.generate_patch_csv_62973F09_62973F09"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
