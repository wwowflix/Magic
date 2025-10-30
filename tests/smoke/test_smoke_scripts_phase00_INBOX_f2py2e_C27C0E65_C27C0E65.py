import importlib, types


def test_import_scripts_phase00_INBOX_f2py2e_C27C0E65_C27C0E65():
    mod = importlib.import_module("scripts.phase00.INBOX.f2py2e_C27C0E65_C27C0E65")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
