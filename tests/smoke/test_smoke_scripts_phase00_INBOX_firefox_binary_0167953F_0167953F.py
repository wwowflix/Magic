import importlib, types


def test_import_scripts_phase00_INBOX_firefox_binary_0167953F_0167953F():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.firefox_binary_0167953F_0167953F"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
