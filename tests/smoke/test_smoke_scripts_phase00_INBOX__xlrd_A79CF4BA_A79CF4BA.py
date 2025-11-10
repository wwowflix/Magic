import importlib, types


def test_import_scripts_phase00_INBOX__xlrd_A79CF4BA_A79CF4BA():
    mod = importlib.import_module("scripts.phase00.INBOX._xlrd_A79CF4BA_A79CF4BA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
