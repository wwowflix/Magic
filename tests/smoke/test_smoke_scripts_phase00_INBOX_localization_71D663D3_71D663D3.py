import importlib, types


def test_import_scripts_phase00_INBOX_localization_71D663D3_71D663D3():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.localization_71D663D3_71D663D3"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
