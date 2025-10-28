import importlib, types

def test_import_scripts_phase00_INBOX_direct_url_2E6201FC_2E6201FC():
    mod = importlib.import_module("scripts.phase00.INBOX.direct_url_2E6201FC_2E6201FC")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
