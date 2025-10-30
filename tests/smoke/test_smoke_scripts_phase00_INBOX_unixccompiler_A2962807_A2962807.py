import importlib, types


def test_import_scripts_phase00_INBOX_unixccompiler_A2962807_A2962807():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.unixccompiler_A2962807_A2962807"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
