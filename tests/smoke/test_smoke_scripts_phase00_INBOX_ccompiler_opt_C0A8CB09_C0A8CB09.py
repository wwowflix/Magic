import importlib, types


def test_import_scripts_phase00_INBOX_ccompiler_opt_C0A8CB09_C0A8CB09():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.ccompiler_opt_C0A8CB09_C0A8CB09"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
