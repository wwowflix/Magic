import importlib, types


def test_import_scripts_phase00_INBOX_hermite_DAFEC814_DAFEC814():
    mod = importlib.import_module("scripts.phase00.INBOX.hermite_DAFEC814_DAFEC814")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
