import importlib, types


def test_import_scripts_phase00_INBOX_cygwinccompiler_E26CEEA3_E26CEEA3():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.cygwinccompiler_E26CEEA3_E26CEEA3"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
