import importlib, types


def test_import_scripts_phase00_INBOX_webelement_EDB77A03_EDB77A03():
    mod = importlib.import_module("scripts.phase00.INBOX.webelement_EDB77A03_EDB77A03")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
