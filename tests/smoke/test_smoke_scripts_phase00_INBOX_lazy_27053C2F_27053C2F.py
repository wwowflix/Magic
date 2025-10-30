import importlib, types


def test_import_scripts_phase00_INBOX_lazy_27053C2F_27053C2F():
    mod = importlib.import_module("scripts.phase00.INBOX.lazy_27053C2F_27053C2F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
