import importlib, types

def test_import_scripts_phase00_INBOX_einsumfunc_3_65979513_65979513():
    mod = importlib.import_module("scripts.phase00.INBOX.einsumfunc_3_65979513_65979513")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
