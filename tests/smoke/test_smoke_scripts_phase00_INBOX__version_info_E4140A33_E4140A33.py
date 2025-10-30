import importlib, types


def test_import_scripts_phase00_INBOX__version_info_E4140A33_E4140A33():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._version_info_E4140A33_E4140A33"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
