import importlib, types


def test_import_scripts_phase00_INBOX_mingw32ccompiler_15F5473F_15F5473F():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.mingw32ccompiler_15F5473F_15F5473F"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
