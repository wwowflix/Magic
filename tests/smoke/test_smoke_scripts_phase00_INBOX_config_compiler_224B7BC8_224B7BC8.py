import importlib, types


def test_import_scripts_phase00_INBOX_config_compiler_224B7BC8_224B7BC8():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.config_compiler_224B7BC8_224B7BC8"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
