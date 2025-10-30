import importlib, types


def test_import_scripts_phase00_INBOX_macromanprober_F5A9DFCE_F5A9DFCE():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.macromanprober_F5A9DFCE_F5A9DFCE"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
