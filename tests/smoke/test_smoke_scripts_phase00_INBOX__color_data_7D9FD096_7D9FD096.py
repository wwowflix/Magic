import importlib, types


def test_import_scripts_phase00_INBOX__color_data_7D9FD096_7D9FD096():
    mod = importlib.import_module("scripts.phase00.INBOX._color_data_7D9FD096_7D9FD096")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
