import importlib, types


def test_import_scripts_phase00_INBOX_pathccompiler_82762106_82762106():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.pathccompiler_82762106_82762106"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
