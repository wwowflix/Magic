import importlib, types


def test_import_scripts_phase00_INBOX_generate_legacy_storage_files_7DAC55A2_7DAC55A2():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.generate_legacy_storage_files_7DAC55A2_7DAC55A2"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
