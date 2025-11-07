import importlib, types


def test_import_scripts_phase00_INBOX__compat_2_DE94B287_DE94B287():
    mod = importlib.import_module("scripts.phase00.INBOX._compat_2_DE94B287_DE94B287")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
