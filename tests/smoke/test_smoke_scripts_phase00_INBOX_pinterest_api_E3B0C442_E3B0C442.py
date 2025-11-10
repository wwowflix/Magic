import importlib, types


def test_import_scripts_phase00_INBOX_pinterest_api_E3B0C442_E3B0C442():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.pinterest_api_E3B0C442_E3B0C442"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
