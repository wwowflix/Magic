import importlib, types


def test_import_scripts_phase00_INBOX_alphabeticalattributes_241A35FD_241A35FD():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.alphabeticalattributes_241A35FD_241A35FD"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
