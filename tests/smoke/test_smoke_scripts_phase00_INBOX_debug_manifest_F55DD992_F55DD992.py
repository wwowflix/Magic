import importlib, types


def test_import_scripts_phase00_INBOX_debug_manifest_F55DD992_F55DD992():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.debug_manifest_F55DD992_F55DD992"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
