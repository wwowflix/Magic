import importlib, types


def test_import_scripts_phase00_INBOX_api_validator_2_F0724091_F0724091():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.api_validator_2_F0724091_F0724091"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
