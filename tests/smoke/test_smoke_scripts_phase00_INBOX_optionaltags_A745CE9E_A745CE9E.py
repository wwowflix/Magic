import importlib, types


def test_import_scripts_phase00_INBOX_optionaltags_A745CE9E_A745CE9E():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.optionaltags_A745CE9E_A745CE9E"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
